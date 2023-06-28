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

if SERVER == SERVER_ENV.DEV.value:
    SECRET_KEY = os.getenv('SECRET_KEY', 'secret')
    DEBUG = os.getenv('DEBUG', True)

    PGRES_DB_NAME = os.getenv('PGRES_DB_NAME', '')
    PGRES_DB_USER = os.getenv('PGRES_DB_USER', '')
    PGRES_DB_PASS = os.getenv('PGRES_DB_PASS', '')
    PGRES_DB_HOST = os.getenv('PGRES_DB_HOST', '')
    PGRES_DB_PORT = os.getenv('PGRES_DB_PORT', '')

    AWS_S3_BUCKET = os.getenv('AWS_S3_BUCKET', '')
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY', '')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_KEY', '')
else:
    # this config is assuming single deployed environment
    SECRET_KEY = ssm.get_parameter(Name='/django/banodoco/secret_key')['Parameter']['Value']
    DEBUG = os.getenv('DEBUG', False)

    PGRES_DB_NAME = ssm.get_parameter(Name='/backend/banodoco/db/name')['Parameter']['Value']
    PGRES_DB_USER = ssm.get_parameter(Name='/backend/banodoco/db/user')['Parameter']['Value']
    PGRES_DB_PASS = ssm.get_parameter(Name='/backend/banodoco/db/password')['Parameter']['Value']
    PGRES_DB_HOST = ssm.get_parameter(Name='/backend/banodoco/db/host')['Parameter']['Value']
    PGRES_DB_PORT = ssm.get_parameter(Name='/backend/banodoco/db/port')['Parameter']['Value']

    AWS_S3_BUCKET = ssm.get_parameter(Name='/backend/neuralblade/aws/s3/bucket')['Parameter']['Value']

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_ALL_ORIGINS = True
CORS_ALLOW_CREDENTIALS = True

CORS_ORIGIN_WHITELIST = [
    'http://localhost:4200',
    'https://banodoco.ai'
    # add any other origins as needed
]

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
    'ai_project'
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


# TODO: add the prod config as well
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
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
