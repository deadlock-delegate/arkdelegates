from datetime import datetime, timedelta

from django.contrib.auth import login, get_user_model
from django.views.generic.base import TemplateView
from django.shortcuts import get_object_or_404, redirect
from app.models import Delegate, ClaimAccointPin
from app.forms import ClaimAccountForm
from app.utils import verify_signature, generate_pin


class ClaimAccount(TemplateView):
    template_name = 'auth/claim_account.html'

    def dispatch(self, request, delegate_slug, *args, **kwargs):
        self.pin = generate_pin()
        self.form = None
        self.delegate = get_object_or_404(Delegate, slug=delegate_slug)
        self.account_already_claimed = False
        return super().dispatch(request, delegate_slug, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        if self.delegate.user_id:
            self.account_already_claimed = True
        else:
            self.form = ClaimAccountForm()
            self._store_generated_pin()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = ClaimAccountForm(request.POST)
        if self.delegate.user_id:
            self.form.add_error(None, 'This account has already been claimed!')
        elif self.form.is_valid():
            data = self.form.cleaned_data['message_json']
            public_key = self.delegate.public_key
            claim_account_data = ClaimAccointPin.objects.get(delegate=self.delegate)

            if claim_account_data.generated_at <= datetime.utcnow() - timedelta(seconds=180):
                self._store_generated_pin()
                self.form.add_error(
                    'message_json',
                    'Your signed pin code has expired. Please try again with a fresh pin code.'
                )
            else:
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

    def _store_generated_pin(self):
        delegate, created = ClaimAccointPin.objects.get_or_create(delegate=self.delegate)
        delegate.pin = self.pin
        delegate.generated_at = datetime.utcnow()
        delegate.save()
