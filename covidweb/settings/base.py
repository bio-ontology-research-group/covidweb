"""
Django settings for covidweb project.

Generated by 'django-admin startproject' using Django 3.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import sys
import shutil
import configparser

from kombu import Exchange, Queue
from django.contrib import messages

# Reading setup properties from configuration file
config_dir = os.path.expanduser("~") + "/.config"
configFile = config_dir + "/covidweb.ini"

if not os.path.isfile(configFile):
    os.makedirs(config_dir, exist_ok=True)
    shutil.copyfile("default_covidweb.ini", configFile)

config = configparser.RawConfigParser()
config.read(configFile)


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Add apps to sys.path
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'pwl+og$a@26+xs8$%_23idz3*$y#8%f-a!qnl%zca_z=sa5)8@'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

ADMINS = [
    ('Maxat Kulmanov', 'coolmaksat@gmail.com'),
]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'accounts',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.keycloak',
    'widget_tweaks',
    'rest_framework',
    'corsheaders',
    'snowpenguin.django.recaptcha2',
    'uploader',
    'sparql'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

CORS_ORIGIN_ALLOW_ALL = True
CSRF_COOKIE_HTTPONLY = True

ROOT_URLCONF = 'covidweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'covidweb.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'covidweb',
        'USER': 'postgres',
        'PASSWORD': '111',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

SESSION_ENGINE = "django.contrib.sessions.backends.cache"

STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.CachedStaticFilesStorage'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

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


# Internationalization
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'public/'
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

MEDIA_ROOT = 'media/'
MEDIA_URL = '/media/'

# User profile module
AUTH_PROFILE_MODULE = 'accounts.models.UserProfile'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_AUTHENTICATION_METHOD = "username_email"
ACCOUNT_EMAIL_VERIFICATION = "none"
ACCOUNT_PRESERVE_USERNAME_CASING = "False"

SITE_ID = 1
SITE_DOMAIN = 'localhost:8000'
SERVER_EMAIL = 'info@bio2vec.net'

# CELERY SETTINGS
CELERY_BROKER_URL = 'redis://localhost:6379/0'
CELERY_ACCEPT_CONTENT = ['json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'

CELERY_RESULT_BACKEND = 'rpc://'
CELERY_WORKER_CONCURRENCY = 24
CELERY_BROKER_POOL_LIMIT = 100
CELERY_BROKER_CONNECTION_TIMEOUT = 10

# configure queues, currently we have only one
CELERY_DEFAULT_QUEUE = 'default'
CELERY_QUEUES = (
    Queue('default', Exchange('default'), routing_key='default'),
)

# Sensible settings for celery
CELERY_ALWAYS_EAGER = False
CELERY_ACKS_LATE = True
CELERY_TASK_PUBLISH_RETRY = True
CELERY_DISABLE_RATE_LIMITS = False

# By default we will ignore result
# If you want to see results and try out tasks interactively, change it to False
# Or change this setting on tasks level
CELERY_IGNORE_RESULT = True
CELERY_SEND_TASK_ERROR_EMAILS = False
CELERY_TASK_RESULT_EXPIRES = 600

FILE_UPLOAD_HANDLERS = [
    # 'django.core.files.uploadhandler.MemoryFileUploadHandler',
    'django.core.files.uploadhandler.TemporaryFileUploadHandler',
]

FILE_UPLOAD_PERMISSIONS = 0o644

RECAPTCHA_PRIVATE_KEY = '6LefajoUAAAAAEiswDUvk1quNKpTJCg49gwrLXpb'
RECAPTCHA_PUBLIC_KEY = '6LefajoUAAAAAOAWkZnaz-M2lgJOIR9OF5sylXmm'
ACCOUNT_FORMS = {
    'login': 'accounts.forms.CaptchaLoginForm',
    'signup': 'accounts.forms.CaptchaSignupForm'}
SOCIALACCOUNT_PROVIDERS = {
    # 'orcid': {
    #     # Base domain of the API. Default value: 'orcid.org', for the production API
    #     'BASE_DOMAIN':'orcid.org',  # for the sandbox API
    #     # Member API or Public API? Default: False (for the public API)
    #     'MEMBER_API': False,  # for the member API
    # },
    'keycloak': {
        'KEYCLOAK_URL': 'https://auth.cdc.gov.sa/auth',
        'KEYCLOAK_REALM': 'GID'
    }
}
SOCIALACCOUNT_AUTO_SIGNUP = True
SOCIALACCOUNT_QUERY_EMAIL = True
# ACCOUNT_ADAPTER = 'accounts.adapter.NoNewUsersAccountAdapter'

MESSAGE_TAGS = {
    messages.INFO: 'list-group-item-info',
    messages.DEBUG: 'list-group-item-info',
    messages.SUCCESS: 'list-group-item-success',
    messages.WARNING: 'list-group-item-warning',
    messages.ERROR: 'list-group-item-danger',
}

VIRTUOSO_HOST=config['virtuoso']['host']
VIRTUOSO_SPARQL_PORT=config['virtuoso']['sparql.port']
VIRTUOSO_USER=config['virtuoso']['user']
VIRTUOSO_PWD=config['virtuoso']['pwd']
RDF_GRAPH_URI=config['virtuoso']['graph']

ABEROWL_API_URL='http://10.254.147.137/api'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'production.log',
        },
        'console': {
            'class': 'logging.StreamHandler',
            'stream': sys.stdout,
        }
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'uploader': {
            'handlers': ['console'],
            'level': 'DEBUG'
        }
    },
}

PANGENOME_RESULT_UUID=config['arvados']['api.pangenome.result.uuid']

ARVADOS_COL_BASE_URI='https://workbench.cborg.cbrc.kaust.edu.sa/collections/'

GALAXY_API_BASEURL=config['galaxy']['api.base_url']
GALAXY_API_KEY=config['galaxy']['api.key']
GALAXY_PANGENOME_RESULT_DIR=config['galaxy']['pangenome_result_dir']
LIBRARY_ID= config['galaxy']['api.library.id']

UPLOADER_PROJECT_UUID = 'cborg-j7d0g-nyah4ques5ww7pk'
