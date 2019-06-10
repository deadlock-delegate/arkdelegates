from datetime import datetime, timedelta

from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.response import Response

from app.forms import ClaimAccountForm
from app.models import ClaimAccointPin, Delegate
from app.utils import generate_pin, verify_signature


class LoginView(KnoxLoginView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class ClaimDelegate(KnoxLoginView):
    authentication_classes = ()
    permission_classes = (permissions.AllowAny,)

    def dispatch(self, request, delegate_slug, *args, **kwargs):
        self.delegate = get_object_or_404(Delegate, slug=delegate_slug)
        self.pin = self._generated_and_store_pin()
        return super().dispatch(request, delegate_slug, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.delegate.user_id:
            return Response({"errors": {"__all__": "Delegate account already claimed"}}, status=400)
        return Response({"pin": self.pin})

    def post(self, request, *args, **kwargs):
        form = ClaimAccountForm(request.data)
        if self.delegate.user_id:
            return Response({"errors": {"__all__": "Delegate account already claimed"}}, status=400)

        elif form.is_valid():
            data = form.cleaned_data["message_json"]

            claim_account_data = ClaimAccointPin.objects.get(delegate=self.delegate)
            if not claim_account_data.pin == data["message"]:
                form.add_error(
                    "message_json",
                    "Your signed pin code has expired. Please try again with a fresh pin code.",
                )
            else:
                public_key = self.delegate.public_key
                is_valid = verify_signature(claim_account_data.pin, public_key, data["signature"])
                if is_valid:
                    password = form.cleaned_data["password"]
                    email = form.cleaned_data["email"]
                    user = get_user_model().objects.create_user(
                        username=self.delegate.slug, email=email, password=password
                    )
                    self.delegate.user = user
                    self.delegate.save()
                    login(request, user)
                    return super().post(request, format=None)

                form.add_error("message_json", "Invalid message and signature!")

        return Response({"errors": form.errors}, status=400)

    def _generated_and_store_pin(self):
        """
        Generates and stores a pin code. If `ClaimAccointPin` code already exist and it was created
        less than 300 sec ago use it, otherwise generate a new one.
        """
        delegate_pin, created = ClaimAccointPin.objects.get_or_create(delegate=self.delegate)
        if not created and delegate_pin.generated_at >= datetime.utcnow() - timedelta(seconds=300):
            pin = delegate_pin.pin
        else:
            pin = generate_pin()
            delegate_pin.pin = pin
            delegate_pin.generated_at = datetime.utcnow()
            delegate_pin.save()
        return pin
