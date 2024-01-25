# This file will contain configurations of the Development version alone. It is sometimes named local.py or dev.py.
from .base import *
from decouple import config


DEBUG = True
ALLOWED_HOSTS = ['127.0.0.1']

INSTALLED_APPS += [
        'debug_toolbar',
    ]

MIDDLEWARE += ['debug_toolbar.middleware.DebugToolbarMiddleware', ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DEBUG_TOOLBAR_CONFIG = {
        'JQUERY_URL': '',
    }

