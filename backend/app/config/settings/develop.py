from datetime import timedelta

from .base import * # noqa


DEBUG = True

INSTALLED_APPS.insert(0, 'django.contrib.admin') # noqa
INSTALLED_APPS.insert(3, 'django.contrib.sessions') # noqa
INSTALLED_APPS.insert(4, 'django.contrib.messages') # noqa
INSTALLED_APPS.insert(5, 'django.contrib.staticfiles') # noqa

MIDDLEWARE.insert(1, 'django.contrib.sessions.middleware.SessionMiddleware') # noqa
MIDDLEWARE.insert(5, 'django.contrib.auth.middleware.AuthenticationMiddleware') # noqa
MIDDLEWARE.insert(6, 'django.contrib.messages.middleware.MessageMiddleware') # noqa

SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'] = timedelta(hours=1) # noqa
