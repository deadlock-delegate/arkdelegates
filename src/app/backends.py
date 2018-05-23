from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend


class CustomModelBackend(ModelBackend):

    def authenticate(self, request, username=None, email=None, password=None):
        User = get_user_model()
        try:
            if username:
                user = User.objects.get(username__iexact=username)
            else:
                user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            user = None

        if user and not user.check_password(password):
            user = None

        return user
