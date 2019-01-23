from decouple import config, Csv

from .base import *

SECRET_KEY = config('SECRET_KEY')

DEBUG = True

ALLOWED_HOSTS = config('ALLOWED_HOSTS', cast=Csv())

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CAPTCHA_TEST_MODE = False

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
