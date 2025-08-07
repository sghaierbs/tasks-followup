from .base import *
import os

DEBUG = True

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'fallback-secret-key')

ALLOWED_HOSTS = [
    'tasks-followup.com',
    'www.tasks-followup.com',
    'localhost',           # optional, for local access
    '127.0.0.1',           # optional, for local access
]
CSRF_TRUSTED_ORIGINS = ['https://tasks-followup.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('POSTGRES_DB', 'tasksfollowup'),
        'USER': os.environ.get('POSTGRES_USER', 'django'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'Nevermind007'),
        'HOST': os.environ.get('POSTGRES_HOST', 'localhost'),
        'PORT': os.environ.get('POSTGRES_PORT', '5432'),
    }
}

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'django-debug.log'),
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}