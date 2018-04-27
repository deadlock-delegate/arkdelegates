import json
from django import forms
from django.contrib.auth import password_validation
from django.core.validators import validate_email
from app.models import Contribution, Delegate, Node, StatusUpdate


class ClaimAccountForm(forms.Form):
    message_json = forms.CharField(widget=forms.Textarea(attrs={'rows': 2}))
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email

    def clean_password(self):
        password = self.cleaned_data.get('password')
        password_validation.validate_password(password)
        return password

    def clean_message_json(self):
        data = self.cleaned_data['message_json']
        try:
            json_data = json.loads(data)
        except:
            raise forms.ValidationError('Invalid data')

        if not (json_data.get('message') and json_data.get('signature')):
            raise forms.ValidationError('JSON does not have an expected structure')

        return json_data


class LoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput)
    password = forms.CharField(widget=forms.PasswordInput)

    def clean_email(self):
        email = self.cleaned_data.get('email')
        validate_email(email)
        return email


class ContributionForm(forms.ModelForm):
    class Meta:
        model = Contribution
        fields = ['title', 'description']


class NodeForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['network', 'cpu', 'memory', 'is_dedicated', 'is_backup']


class ProposalForm(forms.ModelForm):
    class Meta:
        model = Delegate
        fields = ['proposal']


class StatusUpdateForm(forms.ModelForm):
    class Meta:
        model = StatusUpdate
        fields = ['message']
