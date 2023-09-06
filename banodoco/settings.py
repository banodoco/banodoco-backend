import os
from pathlib import Path

import boto3
from util.extended_enum import ExtendedEnum
from dotenv import load_dotenv

load_dotenv()
ssm = boto3.client("ssm", region_name="ap-south-1")

class SERVER_ENV(ExtendedEnum):
    PRODUCTION = 'production'
    DEV = 'development'
    STAGING = 'staging'
    TEST = 'test'

BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ['*']
SERVER = os.getenv('SERVER', SERVER_ENV.DEV.value)
APPEND_SLASH = False

AWS_S3_REGION = 'ap-south-1'
AWS_ACCESS_KEY_ID = None
AWS_SECRET_ACCESS_KEY = None

AMOUNT_TO_CREDITS_MULTIPLIER = 1

if SERVER == SERVER_ENV.DEV.value:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    DEBUG = os.getenv('DEBUG', True)

    DB_NAME = os.getenv('DB_NAME', '')
    DB_USER = os.getenv('DB_USER', '')
    DB_PASS = os.getenv('DB_PASS', '')
    DB_HOST = os.getenv('DB_HOST', '')
    DB_PORT = os.getenv('DB_PORT', '')

    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', '')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY', '')

    GOOGLE_AUTH_CLIENT_ID = os.getenv('GOOGLE_AUTH_CLIENT_ID', '')
    GOOGLE_CLIENT_SECRET = os.getenv('GOOGLE_CLIENT_SECRET', '')
    GOOGLE_AUTH_REDIRECT_URI  = os.getenv('GOOGLE_AUTH_REDIRECT_URI', '')

    ENCRYPTION_KEY = os.getenv('ENCRYPTION_KEY', '')

    STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLIC_KEY', '')
    STRIPE_SECRET_KEY = os.getenv('STRIPE_SECRET_KEY', '')
    STRIPE_WEBHOOK_SECRET = os.getenv('STRIPE_WEBHOOK_SECRET', '')

    REPLICATE_KEY = os.getenv('REPLICATE_KEY', '')
    REPLICATE_UESRNAME = os.getenv('REPLICATE_UESRNAME', '')

    STATIC_AUTH_TOKEN = os.getenv('STATIC_AUTH_TOKEN', '')
else:
    # this config is assuming single deployed environment
    SECRET_KEY = ssm.get_parameter(Name='/django/banodoco/secret_key')['Parameter']['Value']
    DEBUG = os.getenv('DEBUG', False)

    DB_NAME = ssm.get_parameter(Name='/backend/banodoco/db/name')['Parameter']['Value']
    DB_USER = ssm.get_parameter(Name='/backend/banodoco/db/user')['Parameter']['Value']
    DB_PASS = ssm.get_parameter(Name='/backend/banodoco/db/password')['Parameter']['Value']
    DB_HOST = ssm.get_parameter(Name='/backend/banodoco/db/host')['Parameter']['Value']
    DB_PORT = ssm.get_parameter(Name='/backend/banodoco/db/port')['Parameter']['Value']

    AWS_S3_BUCKET = ssm.get_parameter(Name='/backend/banodoco/aws/s3/bucket')['Parameter']['Value']
    AWS_ACCESS_KEY_ID = ssm.get_parameter(Name='/backend/banodoco/aws/access_key')['Parameter']['Value']
    AWS_SECRET_ACCESS_KEY = ssm.get_parameter(Name='/backend/banodoco/aws/access_secret')['Parameter']['Value']

    GOOGLE_AUTH_CLIENT_ID = ssm.get_parameter(Name='/google/auth/client_id')['Parameter']['Value']
    GOOGLE_CLIENT_SECRET = ssm.get_parameter(Name='/google/auth/secret')['Parameter']['Value']
    GOOGLE_AUTH_REDIRECT_URI = ssm.get_parameter(Name='/google/auth/redirect_url')['Parameter']['Value']

    ENCRYPTION_KEY = ssm.get_parameter(Name='/backend/banodoco/encryption/key')['Parameter']['Value']

    STRIPE_PUBLIC_KEY = ssm.get_parameter(Name='/backend/banodoco/stripe/public_key')['Parameter']['Value']
    STRIPE_SECRET_KEY = ssm.get_parameter(Name='/backend/banodoco/stripe/secret_key')['Parameter']['Value']
    STRIPE_WEBHOOK_SECRET = ssm.get_parameter(Name='/backend/banodoco/stripe/webhook_secret')['Parameter']['Value']

    REPLICATE_KEY = ssm.get_parameter(Name='/backend/banodoco/replicate/key')['Parameter']['Value']
    REPLICATE_UESRNAME = ssm.get_parameter(Name='/backend/banodoco/replicate/username')['Parameter']['Value']

    STATIC_AUTH_TOKEN = ssm.get_parameter(Name='/backend/banodoco/auth/static-token')['Parameter']['Value']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

# CORS_ORIGIN_WHITELIST = [
#     'http://localhost:4200',
#     'https://app.banodoco.ai'
#     # add any other origins as needed
# ]

CORS_ALLOW_METHODS = [
    'DELETE',
    'GET',
    'OPTIONS',
    'PATCH',
    'POST',
    'PUT',
]
CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'referer',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'authentication',
    'banodoco',
    'user',
    'ai_project',
    'payment'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'corsheaders.middleware.CorsMiddleware'
]

ROOT_URLCONF = 'banodoco.urls'

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

WSGI_APPLICATION = 'banodoco.wsgi.application'



if SERVER == SERVER_ENV.DEV.value:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3'
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': DB_NAME,
            'USER': DB_USER,
            'PASSWORD': DB_PASS,
            'HOST': DB_HOST,
            'PORT': DB_PORT,
        }
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

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
