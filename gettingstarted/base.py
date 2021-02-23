"""
Django settings for gettingstarted project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os
import json
import six
from six.moves.urllib import request
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
import dj_database_url
#import ssl

CORS_ORIGIN_ALLOW_ALL = True # If this is used then `CORS_ORIGIN_WHITELIST` will not have any effect
CORS_ALLOW_CREDENTIALS = True
ALLOWED_HOSTS = ['127.0.0.1', '0.0.0.0', 'localhost', "http://localhost:3000", "https://localhost:3000"]
CORS_ORIGIN_WHITELIST = ["http://localhost:3000", "https://localhost:3000", "https://localhost:3001", "http://localhost:3001", "https://localhost:3002", "http://localhost:3002", "http://localhost:3002", "http://www.goodneighbor.delivery",  "https://www.goodneighbor.delivery"]

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    #"django.contrib.staticfiles",
    'hello',
    "rest_framework", 
    "rest_framework.authtoken", 
    'rest_framework_jwt',
    'django_extensions',
    'corsheaders',
    'social_django',

]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.RemoteUserMiddleware',
]

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'django.contrib.auth.backends.RemoteUserBackend',
]

JWT_AUTH = {
    'JWT_PAYLOAD_GET_USERNAME_HANDLER':
        'gettingstarted.utils.jwt_get_username_from_payload_handler',
    'JWT_DECODE_HANDLER':
        'gettingstarted.utils.jwt_decode_token',
    'JWT_ALGORITHM': 'RS256',
    'JWT_AUDIENCE': 'https://goodneighbor.us.auth0.com/api/v2/',
    'JWT_ISSUER': 'https://goodneighbor.us.auth0.com/',
    'JWT_AUTH_HEADER_PREFIX': 'Bearer',
}

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.BasicAuthentication',
    ),
}

ROOT_URLCONF = "gettingstarted.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ['resources/templates'],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "gettingstarted.wsgi.application"



# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"
    },
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]


# Internationalization
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = "en-us"

TIME_ZONE = "UTC"

USE_I18N = True

USE_L10N = True

USE_TZ = True

SESSION_COOKIE_SECURE = False
CSRF_COOKIE_SECURE = False


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# STATIC_URL = "/static/"
# STATICFILES_DIRS = [
#     os.path.join(BASE_DIR, 'static')
# ]



# SOCIAL_AUTH_TRAILING_SLASH = False  # Remove trailing slash from routes
# SOCIAL_AUTH_AUTH0_DOMAIN = 'goodneighbor.us.auth0.com'
# SOCIAL_AUTH_AUTH0_KEY = 'X4r4WuvxMbpMNBf7FPZRTCb1Ong9y62x'
# SOCIAL_AUTH_AUTH0_SECRET = 'FAyjQ0AyF3qWmEz6RGC2MgUprADsQSXjkbWVVd4FB4zm3_YWLED0jcIaOE0WIxA9'

# SOCIAL_AUTH_AUTH0_SCOPE = [
#     'openid',
#     'profile',
#     'email'
# ]

# AUTHENTICATION_BACKENDS = {
#     'hello.auth0backend.Auth0',
#     'django.contrib.auth.backends.ModelBackend'
# }

# LOGIN_URL = '/login/auth0'
# LOGIN_REDIRECT_URL = '/dashboard'



