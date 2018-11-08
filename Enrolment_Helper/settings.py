"""
Django settings for Enrolment_Helper project.

Generated by 'django-admin startproject' using Django 1.10.6.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
import sys

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
with open(os.path.join(BASE_DIR, 'SECRET_KEY.txt')) as f:
    SECRET_KEY = f.read().strip()


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# Allow through bridged connection on VM.
ALLOWED_HOSTS = [
]

# Application definition

INSTALLED_APPS = [
    'core_app',
    # 'django_pdb',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'dbbackup',  # django-dbbackup
    'django_cron',
]

CRON_CLASSES = [
    'core_app.cron.Backup',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # 'django_pdb.middleware.PdbMiddleware',
]

ROOT_URLCONF = 'Enrolment_Helper.urls'

PASSWORD_HASHERS = [
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            # '/Users/Eugene/SEP1_Project/2017-11.3-enrolment-helper/templates',
            # '/home/yoakim/UNI/2017/SEP2/',
            # './2017-11.3-enrolment-helper/templates',
            'templates',
        ],
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

WSGI_APPLICATION = 'Enrolment_Helper.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

# Testing takes place on a sqlite database. Significantly faster.
if 'test' in sys.argv:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            # 'OPTIONS': {
            #     'read_default_file': os.path.join(BASE_DIR, 'my.cnf')
            # },
            'NAME': 'Enrolment_Helper',
            'USER': 'enrolment_helperuser',
            'PASSWORD': 'user',
            'HOST': 'localhost',
            'PORT': '',
        },
    }

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Australia/Perth'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'default': {
            'format': '%(asctime)s - %(levelname)s - %(message)s'
            },
        },
    'handlers': {
        'core_app_handler': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'logging.log',
            'formatter': 'default',
        },
        'console': {
            'class': 'logging.StreamHandler',
            },
    },
    'loggers': {
        'core_app': {
            'handlers': ['core_app_handler'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}
# Default page
LOGIN_URL = '/login/'

# Save database to this file path
DBBACKUP_STORAGE = 'django.core.files.storage.FileSystemStorage'
DBBACKUP_STORAGE_OPTIONS = {'location': '/home/hannes/ENROLMENT_HELPER/backups/'}

# Backend is for smtp email sever
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

# Host is setup for email
EMAIL_HOST = 'smtp.gmail.com'

EMAIL_USE_TLS = True

# User is email address in form from@example.com
EMAIL_HOST_USER = 'etracker.notification@gmail.com'

# Password of email
EMAIL_HOST_PASSWORD = 'ihatebears18'

# Port to send
EMAIL_PORT = 587
