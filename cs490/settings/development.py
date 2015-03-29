"""
Django settings for cs490 project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import secrets
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's1h=i5$z89!gi1&4046h58c9&*g)6!@&y&b^ch2m=nzt=#m5sd'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition
DJANGO_APPS = (
	    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
)

THIRD_PARTY_APPS = (
	'taggit',
    'guardian',
    'crispy_forms',
    'haystack',
    'randomslugfield',
)

LOCAL_APPS = (
	'accounts',
    'core',
    'qa',
    'registration',

)

HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.simple_backend.SimpleEngine',
    },
}

TEMPLATED_EMAIL_BACKEND = 'templated_email.backends.vanilla_django'

CRISPY_TEMPLATE_PACK = 'bootstrap3'


INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'django_cas_ng.backends.CASBackend',
    'guardian.backends.ObjectPermissionBackend',
)

ANONYMOUS_USER_ID = -1

ROOT_URLCONF = 'cs490.urls'

WSGI_APPLICATION = 'cs490.wsgi.application'

#######
####CAS SETTINGS#######
CAS_SERVER_URL = secrets.CAS_URL
CAS_REDIRECT_URL = 'http://localhost:8000/'
CAS_LOGOUT_COMPLETELY = True
#######END CAS SETTINGS##############

LOGIN_REDIRECT_URL = '/accounts/new'

ORGANIZATION_EMAIL_DOMAIN = 'masonlive.gmu.edu'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_PORT = 587
EMAIL_HOST_USER = secrets.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = secrets.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = True

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, '../../db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATICFILES_FINDERS = (
	'django.contrib.staticfiles.finders.FileSystemFinder',
	'django.contrib.staticfiles.finders.AppDirectoriesFinder',  # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

MEDIA_ROOT = '/tmp/'
MEDIA_URL = '/file/'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = 'static'


STATICFILES_DIRS = (
    'bower_components',
)

TEMPLATE_DIRS = (
	'templates',
    'core/templates',
    'registration/templates',
    'accounts/templates',
)