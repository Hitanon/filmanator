from datetime import timedelta
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent.parent

env = environ.Env(
    # Django
    SECRET_KEY=(str, 'django-secret-key'),
    ALLOWED_HOST=(str, 'localhost'),
    CORS_ALLOWED_ORIGINS=(str, 'http://localhost'),

    # Database
    DB_NAME=(str, 'DB_NAME'),
    DB_USER=(str, 'DB_USER'),
    DB_PASSWORD=(str, 'DB_PASSWORD'),
    DB_HOST=(str, 'DB_HOST'),
    DB_PORT=(int, 'DB_PORT'),

    # Parser
    TOKEN=(str, 'TOKEN'),
    START_PAGE=(int, 1),
    END_PAGE=(int, 10),
    LIMIT=(int, 1000),
    UPDATE=(bool, False),

    # ChatGPT
    FULL_PATH_TO_FILES=(str, 'PATH'),

    # Questionnaire
    QUESTIONNAIRE_FILE_PATH=(str, ''),
    CATEGORIES_LIMIT=(int, 0),

    # Redis
    REDIS_PORT=(int, 6379),
    REDIS_HOST=(str, '0.0.0.0'),
)

env.read_env(BASE_DIR.parent / '.env')

SECRET_KEY = env('SECRET_KEY')

ALLOWED_HOSTS = [
    env('ALLOWED_HOST'),
]

CONN_MAX_AGE = 60

AUTH_USER_MODEL = 'users.User'

# Parser
TOKEN = env('TOKEN')
START_PAGE = env('START_PAGE')
END_PAGE = env('END_PAGE')
LIMIT = env('LIMIT')
UPDATE = env('UPDATE')

# ChatGPT
FULL_PATH_TO_FILES = env('FULL_PATH_TO_FILES')

# CORS
CORS_ALLOWED_ORIGINS = [
    env('CORS_ALLOWED_ORIGINS') if env('CORS_ALLOWED_ORIGINS') else 'http://localhost',
]

# Questionnaire
QUESTIONNAIRE_FILE_PATH = env('QUESTIONNAIRE_FILE_PATH')
CATEGORIES_LIMIT = env('CATEGORIES_LIMIT')
SESSION_LIFETIME = timedelta(hours=1)

# Redis
REDIS_PORT = env('REDIS_PORT')
REDIS_HOST = env('REDIS_HOST')

# Celery
CELERY_BROKER_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:{REDIS_PORT}/1'

INSTALLED_APPS = [
    # Встроенные django приложения
    'django.contrib.auth',
    'django.contrib.contenttypes',

    # Дополнительные django приложения
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',

    # Приложения проекта
    'questionnaire',
    'titles',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': env('DB_NAME'),
        'USER': env('DB_USER'),
        'PASSWORD': env('DB_PASSWORD'),
        'HOST': env('DB_HOST'),
        'PORT': env('DB_PORT'),
    },
}

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_RENDERER_CLASSES': (
            'rest_framework.renderers.JSONRenderer',
            'rest_framework.renderers.BrowsableAPIRenderer',
    ),
}

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': False,

    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,

    'VERIFYING_KEY': '',
    'AUDIENCE': None,
    'ISSUER': None,
    'JSON_ENCODER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken', ),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    'SLIDING_TOKEN_REFRESH_EXP_CLAIM': 'refresh_exp',
    'SLIDING_TOKEN_LIFETIME': timedelta(minutes=5),
    'SLIDING_TOKEN_REFRESH_LIFETIME': timedelta(days=1),

    'TOKEN_OBTAIN_SERIALIZER': 'users.serializers.CustomTokenObtainPairSerializer',
    'TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSerializer',
    'TOKEN_VERIFY_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenVerifySerializer',
    'TOKEN_BLACKLIST_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenBlacklistSerializer',
    'SLIDING_TOKEN_OBTAIN_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenObtainSlidingSerializer',
    'SLIDING_TOKEN_REFRESH_SERIALIZER': 'rest_framework_simplejwt.serializers.TokenRefreshSlidingSerializer',
}
