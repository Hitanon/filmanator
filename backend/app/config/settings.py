from datetime import timedelta
from pathlib import Path

import environ


BASE_DIR = Path(__file__).resolve().parent.parent

env = environ.Env(
    # Django
    DEBUG=(bool, True),
    SECRET_KEY=(str, 'django-secret-key'),
    ALLOWED_HOST=(str, 'localhost'),

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
)

env.read_env(BASE_DIR.parent / '.env')

SECRET_KEY = env('SECRET_KEY')

DEBUG = env('DEBUG')

ALLOWED_HOSTS = [
    env('ALLOWED_HOST'),
]

INSTALLED_APPS = [
    # Встроенные django приложения
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Дополнительные django приложения
    'django_extensions',

    # Приложения проекта
    'questionnaire',
    'titles',
    'users',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True

STATIC_URL = 'static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

AUTH_USER_MODEL = 'users.User'

SESSION_LIFETIME = timedelta(hours=1)

# Parser
TOKEN = env('TOKEN')
START_PAGE = env('START_PAGE')
END_PAGE = env('END_PAGE')
LIMIT = env('LIMIT')
UPDATE = env('UPDATE')

# ChatGPT
FULL_PATH_TO_FILES = env('FULL_PATH_TO_FILES')
