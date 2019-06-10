"""
Django settings for galaxy_api project.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import sys

from dynaconf import LazySettings

# --- BEGIN OF DYNACONF HEADER ---
settings = LazySettings(
    GLOBAL_ENV_FOR_DYNACONF='GALAXY',
)
# --- END OF DYNACONF HEADER ---

ALLOWED_HOSTS = []

# Application definition
INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'rest_framework',

    'galaxy_common.apps.AppConfig',
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

ROOT_URLCONF = 'galaxy_api.urls'

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


WSGI_APPLICATION = 'galaxy_api.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': settings.get('DB_NAME', 'galaxy'),
        'USER': settings.get('DB_USER', 'galaxy'),
        'PASSWORD': settings.get('DB_PASSWORD', ''),
        'HOST': settings.get('DB_HOST', 'localhost'),
        'PORT': settings.get('DB_PORT', ''),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'

# API settings

API_PATH_PREFIX = 'api'

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': (
        'rest_framework.renderers.JSONRenderer',
    )
}

# Celery settings

CELERY_BROKER_URL = 'amqp://{user}:{password}@{host}:{port}/{vhost}'.format(
    user=settings.get('RABBITMQ_USER', 'galaxy'),
    password=settings.get('RABBITMQ_PASSWORD', ''),
    host=settings.get('RABBITMQ_HOST', 'localhost'),
    port=settings.get('RABBITMQ_PORT', 5672),
    vhost=settings.get('RABBITMQ_VHOST', 'galaxy'),
)

# --- BEGIN OF DYNACONF FOOTER ---
settings.populate_obj(sys.modules[__name__])
# --- END OF DYNACONF FOOTER ---
