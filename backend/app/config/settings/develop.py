from .base import * # noqa

DEBUG = True

INSTALLED_APPS.insert(9, 'debug_toolbar') # noqa

MIDDLEWARE.insert(0, 'debug_toolbar.middleware.DebugToolbarMiddleware') # noqa
