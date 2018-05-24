from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django.views.generic.base import TemplateView

from app.forms import LoginForm


class Login(TemplateView):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('delegate', delegate_slug=self.request.user.delegate.slug)
        self.form = LoginForm()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.form = LoginForm(request.POST)
        if self.form.is_valid():
            password = self.form.cleaned_data['password']
            email = self.form.cleaned_data['email']
            user = authenticate(email=email, password=password)
            if not user:
                self.form.add_error(
                    None,
                    'Please enter a correct email and password. Note that both fields '
                    'are case-sensitive.'
                )
            elif not user.is_active:
                self.form.add_error(None, 'Sorry, this account is inactive.')
            else:
                login(request, user)
                return redirect('delegate', delegate_slug=user.delegate.slug)
        return super().render_to_response(self.get_context_data())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context.update({
            'form': self.form,
        })

        return context
