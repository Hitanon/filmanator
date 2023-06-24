from .base import * # noqa

DEBUG = True

INSTALLED_APPS.insert(6, 'django_extensions') # noqa
INSTALLED_APPS.insert(10, 'debug_toolbar') # noqa

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware') # noqa
