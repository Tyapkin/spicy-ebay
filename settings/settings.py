import os
from celery.schedules import crontab

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '(op6ksp@a*-kl%m@tn=r^r7u%c7u)7fzz%^#5f*3#yjt_m-6g)'

ALLOWED_HOSTS = ['127.0.0.1', 'localhost']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'apps.accounts',
    'apps.ebay_catalog',
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

ROOT_URLCONF = 'settings.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.abspath(os.path.join(BASE_DIR, 'templates'))],
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

WSGI_APPLICATION = 'settings.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'spicy',
        'USER': 'root',
        'PASSWORD': 'admin1',
        'HOST': 'localhost',
        'PORT': '5432',
        'TEST': {
            'CHARSET': 'utf8',
            'COLLATION': 'utf8_general_ci',
        }
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/1.11/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/

STATIC_URL = '/static/'
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.abspath(os.path.join(BASE_DIR, 'media'))
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'assets'),)
DOWNLOADABLE_FILES = os.path.abspath(os.path.join(BASE_DIR, 'files'))


# registration
ACCOUNT_ACTIVATION_DAYS = 7
LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/ebay-catalog/'
LOGOUT_URL = '/accounts/logout/'
LOGOUT_REDIRECT_URL = LOGIN_URL


# ebay api
PRODUCTION_ENDPOINT = 'http://svcs.ebay.com/services/search/FindingService/v1'
SANDBOX_ENDPOINT = 'http://svcs.sandbox.ebay.com/services/search/FindingService/v1'
SHOPPING_API_ENDPOINT = 'http://open.api.ebay.com/shopping'


# CELERY settings
BROKER_URL = 'redis://localhost:6379'
CELERY_RESULT_BACKEND = 'redis://localhost:6379'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'Europe/Kiev'

CELERYBEAT_SCHEDULE = {
    'auto_update_every_five_minutes': {
        'task': 'apps.ebay_catalog.tasks.auto_update_all_products',
        'schedule': crontab(minute='*/5'),
    },
}


# logging settings
LOG_FILE = os.path.join(BASE_DIR, 'spicy_ebay_log.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s',
            'datefmt': '%Y/%m/%d %H:%M:%S'
        },
        'simple': {
            'format': '%(levelname)s: %(message)s'
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': LOG_FILE,
            'maxBytes': 500000,
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'apps.ebay_catalog': {
            'handlers': ['file', 'console'],
            'propagate': True,
            'level': 'DEBUG'
        },
        'apps.accounts': {
            'handlers': ['file'],
            'propagate': True,
            'level': 'INFO'
        }
    }
}


# trying import settings
try:
    from .production import *
except ImportError as e:
    from .development import *
