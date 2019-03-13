"""
Django settings for vinestream project.

Generated by 'django-admin startproject' using Django 2.0.6.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""
from django.urls import reverse_lazy
import os


from decouple import config, Csv
import dj_database_url

SECRET_KEY = config('SECRET_KEY', default='xe%h)vvlc&qx9#aql&02^kboq244nq)+9ml%qrje*ex$1u#7wz')
DEBUG = config('DEBUG', default=False, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())
DATABASES = {
    'default': dj_database_url.config(
        default=config('DATABASE_URL')
    )
}
EMAIL_BACKEND = config('EMAIL_BACKEND', default='django.core.mail.backends.smtp.EmailBackend')
EMAIL_HOST = config('EMAIL_HOST', default='')
EMAIL_PORT = config('EMAIL_PORT', default=587, cast=int)
EMAIL_HOST_USER = config('EMAIL_HOST_USER', default='')
EMAIL_HOST_PASSWORD = config('EMAIL_HOST_PASSWORD', default='')
EMAIL_USE_TLS = config('EMAIL_USE_TLS', default=True, cast=bool)

DEFAULT_FROM_EMAIL = 'StarDaf <noreply@stardaf.com>'
EMAIL_SUBJECT_PREFIX = '[StarDaf] '


EMAIL_HOST='smtp.mailgun.org'
EMAIL_PORT=587
EMAIL_HOST_USER='postmaster@mg.stardaf.com'
EMAIL_HOST_PASSWORD='c3a8f3439f9f751908be125be0271825-c8c889c9-027676c8'
EMAIL_USE_TLS=True
EMAIL_USE_SSL =False

# __AUTHOR__ = 'Faisal Lawan Muhammad'

# ABSOLUTE_URL_OVERRIDES = {
#          'auth.user': lambda u: reverse_lazy('account:profile',
#          args=[u.id, u.username]) 
#  }

ABSOLUTE_URL_OVERRIDES = {
         'auth.user': lambda u: reverse_lazy('account:profile',
         args=[u.username])
 }

LOGIN_URL = reverse_lazy('account:register')
LOGIN_REDIRECT_URL = reverse_lazy('account:stream')
LOGOUT_URL = reverse_lazy('account:logout')

PAYSTACK_FAILED_URL = reverse_lazy('order:order_create')
PAYSTACK_SUCCESS_URL =  reverse_lazy('account:success')


# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'xe%h)vvlc&qx9#aql&02^kboq244nq)+9ml%qrje*ex$1u#7wz'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'paystack',
    #'channels',
    'chat',
    'action',
    'Comment',
    'order',
    'cart',
    'bizz',
    'widget_tweaks',
    'account',
    'django.contrib.postgres',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'sorl.thumbnail',
]
THUMBNAIL_DEBUG = True
TEMPLATE_DEBUG = True

# free_wifi_password = '</a>' </a>pas55w0rd

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'vinestream.urls'
#ASGI_APPLICATION = "vinestream.routing.application"

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
                'cart.context_processors.cart',
                'django.template.context_processors.media',
            ],
        },
    },
]

WSGI_APPLICATION = 'vinestream.wsgi.application'



# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

# default database
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#     }
# }

#postgreSql database (development)
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'vinestream',
#         'USER': 'postgres',
#         'PASSWORD': 'faisal',
#     }
# }


# production database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stardaf',
        'USER': 'u_faisal',
        'PASSWORD': '0completehuman0',
        'HOST':'localhost',
        'port':'',

    }
}


# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'vinestream',
#         'USER': 'postgres',
#         'PASSWORD': 'faisal',
#     }
# }


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

STATIC_ROOT = os.path.join(BASE_DIR, 'account/static/')
STATIC_URL = '/static/'
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

CART_SESSION_ID = 'cart'

REDIS_HOST = 'localhost'
REDIS_PORT = 6379
REDIS_DB = 0


AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'account.authentication.EmailAuthBackend',
 )

# ASGI_APPLICATION = "vinestream.routing.application"

# CHANNEL_LAYERS = {
#     "default": {
#         "BACKEND": "channels_redis.core.RedisChannelLayer",
#         "CONFIG": {
#             "hosts": [("localhost", 6379)],
#         },
#     },
# }

PAYSTACK_PUBLIC_KEY = 'pk_live_f4d4dee55901a2ec83276902a9177ba992385dd6'
PAYSTACK_SECRET_KEY = 'sk_live_e67a92c91daa54023f726273aadfacf2f0b62959'
