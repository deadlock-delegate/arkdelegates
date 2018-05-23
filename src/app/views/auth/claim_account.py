from datetime import datetime, timedelta

from django.contrib.auth import get_user_model, login
from django.shortcuts import get_object_or_404, redirect
from django.views.generic.base import TemplateView

from app.forms import ClaimAccountForm
from app.models import ClaimAccointPin, Delegate
from app.utils import generate_pin, verify_signature


class ClaimAccount(TemplateView):
    template_name = 'auth/claim_account.html'

    def dispatch(self, request, delegate_slug, *args, **kwargs):
        self.form = None
        self.delegate = get_object_or_404(Delegate, slug=delegate_slug)
        self.pin = self._generated_and_store_pin()
        self.account_already_claimed = False
        return super().dispatch(request, delegate_slug, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.delegate.user_id:
            self.account_already_claimed = True
        else:
            self.form = ClaimAccountForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = ClaimAccountForm(request.POST)
        if self.delegate.user_id:
            self.form.add_error(None, 'This account has already been claimed!')
        elif self.form.is_valid():
            data = self.form.cleaned_data['message_json']

            claim_account_data = ClaimAccointPin.objects.get(delegate=self.delegate)
            if not claim_account_data.pin == data['message']:
                self.form.add_error(
                    'message_json',
                    'Your signed pin code has expired. Please try again with a fresh pin code.'
                )
            else:
                public_key = self.delegate.public_key
                is_valid = verify_signature(claim_account_data.pin, public_key, data['signature'])
                if is_valid:
                    password = self.form.cleaned_data['password']
                    email = self.form.cleaned_data['email']
                    user = get_user_model().objects.create_user(
                        username=self.delegate.slug,
                        email=email,
                        password=password
                    )
                    self.delegate.user = user
                    self.delegate.save()
                    login(request, user)
                    return redirect('delegate', delegate_slug=self.delegate.slug)
                self.form.add_error('message_json', 'Invalid message and signature!')

        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'pin': self.pin,
            'delegate': self.delegate,
            'form': self.form,
            'account_already_claimed': self.account_already_claimed
        })

        return context

    def _generated_and_store_pin(self):
        """
        Generates and stores a pin code. If `ClaimAccointPin` code already exist and it was created
        less than 180sec ago use it, otherwise generate a new one.
        """
        delegate_pin, created = ClaimAccointPin.objects.get_or_create(delegate=self.delegate)
        if not created and delegate_pin.generated_at >= datetime.utcnow() - timedelta(seconds=180):
            pin = delegate_pin.pin
        else:
            pin = generate_pin()
            delegate_pin.pin = pin
            delegate_pin.generated_at = datetime.utcnow()
            delegate_pin.save()
        return pin
