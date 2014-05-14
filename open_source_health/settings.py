"""
Django settings for open_source_health project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'b%&%wu@a!q^$7n_qw3^_zzss39en_ingo_66e-dnmcyizu!u+d'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True




# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'social.apps.django_app.default',
    'categories',
    'projects',
    'accounts',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'social.apps.django_app.middleware.SocialAuthExceptionMiddleware',
)

ROOT_URLCONF = 'open_source_health.urls'

WSGI_APPLICATION = 'open_source_health.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases
# need to change to postgresql
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'osh_db',
        'USER': 'wulfe',
        'PASSWORD': 'iceo',
        'HOST': 'localhost',
        'PORT': '',
    }
}

# Template Locations
TEMPLATE_DIRS = (
    BASE_DIR + '/open_source_health/templates/',
    BASE_DIR + '/categories/templates/',
    BASE_DIR + '/projects/templates/',
    BASE_DIR + '/accounts/templates/',
    )

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Parse database configuration from $DATABASE_URL
# import dj_database_url
# DATABASES['default'] =  dj_database_url.config()

# Honor the 'X-Forwarded-Proto' header for request.is_secure()
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

# Allow all host headers
ALLOWED_HOSTS = ['*']

# Static asset configuration
import os
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
STATIC_ROOT = 'staticfiles'
STATIC_URL = '/static/'

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, 'static'),
    'static',
)

AUTHENTICATION_BACKENDS = (
    'social.backends.github.GithubOAuth2',
    'django.contrib.auth.backends.ModelBackend',
  )
SOCIAL_AUTH_GITHUB_KEY = 'c7e158382b6aa37d14a9'
SOCIAL_AUTH_GITHUB_SECRET = '61a4c3bf5ff25c7c8b688c10b5f3badb4d56e9c6'
TEMPLATE_CONTEXT_PROCESSORS = (
    'social.apps.django_app.context_processors.backends',
    'social.apps.django_app.context_processors.login_redirect',
    'django.contrib.auth.context_processors.auth',
)

LOGIN_URL = '/accounts/login/'
LOGIN_REDIRECT_URL = '/accounts'
DISCONNECT_REDIRECT_URL = '/categories/by_group'
URL_PATH = ''
SOCIAL_AUTH_GITHUB_SCOPE = ['user:email']

SOCIAL_AUTH_STRATEGY = 'social.strategies.django_strategy.DjangoStrategy'
SOCIAL_AUTH_STORAGE = 'social.apps.django_app.default.models.DjangoStorage'
#SOCIAL_AUTH_USER_MODEL = 'django.contrib.auth.models.User'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'standard': {
            'format': '%(message)s \n\n\n'
        },
    },
    'handlers': {
        'default': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': 'logs/mylog.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter':'standard',
        },  
        # 'request_handler': {
        #         'level':'DEBUG',
        #         'class':'logging.handlers.RotatingFileHandler',
        #         'filename': 'logs/django_request.log',
        #         'maxBytes': 1024*1024*5, # 5 MB
        #         'backupCount': 5,
        #         'formatter':'standard',
        # },
    },
    'loggers': {

        'log': {
            'handlers': ['default'],
            'level': 'INFO',
            'propagate': False
        },
        # 'django.request': {
        #     'handlers': ['request_handler'],
        #     'level': 'DEBUG',
        #     'propagate': False
        # },
    }
}
