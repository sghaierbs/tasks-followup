from .base import *

DEBUG = True
ALLOWED_HOSTS = []

# Simple sqlite for dev
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'taradhidb'),
        'USER': os.environ.get('POSTGRES_USER', 'taradhi'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'Nevermind007'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

# Optionally use console email backend for dev
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
