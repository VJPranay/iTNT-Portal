import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-68bn2*xnujz@*i2(xb61^kk3vhzo8sfyw3mrn7***srqkm49_*'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False
DEV = False

ALLOWED_HOSTS = [
'itnthub.tn.gov.in',
'127.0.0.1',
]

CSRF_TRUSTED_ORIGINS = [ 
    'https://itnthub.tn.gov.in',
    'http://127.0.0.1'
]

SESSION_COOKIE_SECURE = True

CSRF_COOKIE_SECURE = True



# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'registrations',
    'profiles',
    'innovation_challenges',
    'custom_ic',
    'analytics',
    'meetings',
    'datarepo',
    'django_extensions',
    'marketplace',
    'dashboard',
    'common',
    'support',
    'reports',
    'crispy_forms',
    'crispy_bootstrap5',
    'import_export',
    'django_filters',
]

AUTH_USER_MODEL = 'profiles.User'

MIDDLEWARE = [
        #'csp.middleware.CSPMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'ldevcatalyst.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates')
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

WSGI_APPLICATION = 'ldevcatalyst.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.0/ref/settings/#databases

if DEV:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }
else:
    FORCE_SCRIPT_NAME = '/innovation-portal'
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'tempordb',
            'USER': 'temporusr',
            'PASSWORD': 'J35u53253#@%#',
            'HOST': '10.236.205.46',
            'PORT': '5432',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE =  'Asia/Kolkata'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.0/howto/static-files/

#STATIC_URL = 'static/'
#STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static')]
MEDIA_URL = '/innovation-portal/media/'
MEDIA_ROOT = '/opt/portal/iTNT-Portal/ldevcatalyst/virtualdisk/'
DEFAULT_FILE_STORAGE = 'django.core.files.storage.FileSystemStorage'

#STATIC_ROOT = os.path.join(BASE_DIR, 'static')


#import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
#BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/innovation-portal/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# The absolute path to the directory where collectstatic will collect static files for deployment.
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Default primary key field type
# https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

LOGIN_URL = '/dashboard/'
LOGOUT_URL = '/dashboard/logout/'
#LOGIN_REDIRECT_URL = '/dashboard/index/'
LOGIN_FAILURE_URL = '/dashboard/'





EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'mail.tn.gov.in'
EMAIL_USE_TLS = True
email_port = 465
EMAIL_HOST_FROM = 'aso.itnt@tn.gov.in'

EMAIL_HOST_EMAIL = 'aso.itnt@tn.gov.in'
EMAIL_HOST_USER = 'aso.itnt'
EMAIL_HOST_USERNAME = 'aso.itnt'
EMAIL_RECEIVER_USER = 'aso.itnt@tn.gov.in'
EMAIL_HOST_PASSWORD = "uheim}a3"
CUSTOM_SMTP_HOST = 'mail.tn.gov.in'
CUSTOM_SMTP_SENDER = 'aso.itnt@tn.gov.in'
CUSTOM_SMTP_USERNAME = 'aso.itnt'
CUSTOM_SMTP_PASSWORD = 'uheim}a3'
email_host = 'mail.tn.gov.in'
email_port = 465
email_username = 'aso.itnt'
email_from = 'aso.itnt@tn.gov.in'
email_password = 'uheim}a3'
CRISPY_ALLOWED_TEMPLATE_PACKS = "bootstrap5"
CRISPY_TEMPLATE_PACK = "bootstrap5"
DATA_UPLOAD_MAX_MEMORY_SIZE = 100 * 1024 * 1024
