from .base import *

DEBUG = True

INSTALLED_APPS.insert(9, 'django_extensions')
INSTALLED_APPS.insert(10, 'debug_toolbar')

MIDDLEWARE.insert(1, 'debug_toolbar.middleware.DebugToolbarMiddleware')

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}


LOGGING = {
    'version': 1,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'django.db.backends': {
            'level': 'DEBUG',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}
