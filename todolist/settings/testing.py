from decouple import config, Csv

from .base import *

SECRET_KEY = '*xtipyb*z!q*!  # wnca_q-2063m)+*80r2n=x)0i5sf=tafj21z'

ALLOWED_HOSTS = []

DEBUG = True

CAPTCHA_TEST_MODE = True

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
