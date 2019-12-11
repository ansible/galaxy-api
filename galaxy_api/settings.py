"""Project settings."""

import sys

from dynaconf import LazySettings


# --- BEGIN OF DYNACONF HEADER ---
settings = LazySettings(
    GLOBAL_ENV_FOR_DYNACONF='GALAXY',

)
# --- END OF DYNACONF HEADER ---

# ---------------------------------------------------------
# Django settings
# ---------------------------------------------------------
ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.messages',
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'rest_framework',
    'django_filters',

    'galaxy_api.api',
    'galaxy_api.auth',
]

MIDDLEWARE = [
    'request_id.middleware.RequestIdMiddleware',

    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

]

ROOT_URLCONF = 'galaxy_api.urls'

AUTH_USER_MODEL = 'galaxy_auth.user'

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

# Database

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'

# ---------------------------------------------------------
# Third party libraries settings
# ---------------------------------------------------------

# Rest Framework

REST_FRAMEWORK = {
    'DEFAULT_RENDERER_CLASSES': [
        'rest_framework.renderers.JSONRenderer',
    ],
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'galaxy_api.auth.auth.RHIdentityAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'galaxy_api.auth.auth.RHEntitlementRequired',
    ],
    'DEFAULT_PAGINATION_CLASS': 'galaxy_api.api.pagination.LimitOffsetPagination',
    'EXCEPTION_HANDLER': 'galaxy_api.api.exceptions.exception_handler',
}

RH_ENTITLEMENT_REQUIRED = 'insights'

# ---------------------------------------------------------
# Application settings
# ---------------------------------------------------------

API_PATH_PREFIX = 'api/automation-hub'

PULP_API_HOST = 'pulp-api'
PULP_API_PORT = 8000
PULP_API_USER = 'admin'
PULP_API_PASSWORD = 'admin'

PULP_CONTENT_HOST = 'pulp-content-app'
PULP_CONTENT_PORT = 24816
PULP_CONTENT_PATH_PREFIX = '/api/automation-hub/v3/artifacts/collections/'

# CLOUD_WATCH_LOGGER = {
#     'AWS_ACCESS_KEY_ID': '',
#     'AWS_SECRET_ACCESS_KEY': '',
#     'AWS_REGION_NAME': '',
#     'LOGGING_GROUP': '',
#     'LOGGING_STREAM_NAME': ''
# }

# ---------------------------------------------------------
# Logging settings
# ---------------------------------------------------------

# CloudWatch logging example:
# LOGGING = {
#     ...
#     'handlers': {
#         'cloudwatch': {
#             'class': 'galaxy_api.contrib.logging.CloudWatchHandler',
#         },
#     }
#     ...
# }

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s %(levelname)s %(name)s: %(message)s',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'root': {
        'level': 'WARNING',
        'handlers': ['console'],
    },
    'loggers': {
        'django': {
            # NOTE: Override django built-in handler.
            'propagate': True,
        },
        'django.server': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    }
}

################################################################################
#                                   FOOTER                                     #
################################################################################
# --- BEGIN OF DYNACONF FOOTER ---
settings.populate_obj(sys.modules[__name__])
# --- END OF DYNACONF FOOTER ---
