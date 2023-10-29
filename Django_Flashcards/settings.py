"""
Django settings for Django_Flashcards project.

Generated by 'django-admin startproject' using Django 3.1.

For more information on this file, see
https://docs.djangoproject.com/en/3.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.1/ref/settings/
"""

from pathlib import Path
import os
import dj_database_url


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '^k30iw)$-5^^q*p*3%t5!z6aa3e$@^48t^x=z3y+&r8-f$-k)='
#SECRET_KEY = os.environ.get('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['127.0.0.1',"*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'flashcards',
    'crispy_forms',
    'users',
]
CRISPY_TEMPLATE_PACK = 'bootstrap4'


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    #'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'Django_Flashcards.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / "templates"],
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
APP_1_TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'flashcards', 'templates'),
]

APP_2_TEMPLATE_DIRS = [
    os.path.join(BASE_DIR, 'users', 'templates'),
]

TEMPLATES[0]['DIRS'] += APP_1_TEMPLATE_DIRS
TEMPLATES[0]['DIRS'] += APP_2_TEMPLATE_DIRS

WSGI_APPLICATION = 'Django_Flashcards.wsgi.application'


# Database 
# https://docs.djangoproject.com/en/3.1/ref/settings/#databases

DATABASES = {
    'default': dj_database_url.parse("postgres://flashcard_maker_user:1tEnGXycgtUmIDBhhJ5sEGE0PZeAgVpL@dpg-ckv9nsq37rbc73foklt0-a.oregon-postgres.render.com/flashcard_maker")
}

'''DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'Flashcards',
        'USER': 'Abhi',
        'PASSWORD': 'Abhi@1404',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}'''






# Password validation
# https://docs.djangoproject.com/en/3.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.1/howto/static-files/

PROJECT_ROOT = os.path.abspath(os.path.dirname(__file__))

STATIC_URL = '/static/'

MEDIA_URL = '/images/'

STATICFILES_DIRS = [
    os.path.join(PROJECT_ROOT, 'static')
]

MEDIA_ROOT = os.path.join(BASE_DIR, 'static/images')

CRISPY_TEMPLATE_PACK = 'bootstrap4'

LOGIN_REDIRECT_URL = 'home'
LOGIN_URL = 'login'


# ------------------------------------------------------------
# For Heroku deployement
# DEBUG = False
# ALLOWED_HOSTS = ['djangoflashcardsmaker.herokuapp.com', '127.0.0.1']
# in MIDDLEWARE var: uncomment  'whitenoise.middleware.WhiteNoiseMiddleware',
# STATIC_ROOT = os.path.join(PROJECT_ROOT, 'staticfiles')
# import django_heroku
# django_heroku.settings(locals())
