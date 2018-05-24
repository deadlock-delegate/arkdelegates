"""
WSGI config for a project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/howto/deployment/wsgi/
"""
from django.core.wsgi import get_wsgi_application

from raven.contrib.django.raven_compat.middleware.wsgi import Sentry

from whitenoise.django import DjangoWhiteNoise


def get_application():
    application = get_wsgi_application()
    application = Sentry(application)
    application = DjangoWhiteNoise(application)
    return application
