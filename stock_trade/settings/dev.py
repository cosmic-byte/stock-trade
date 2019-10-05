from stock_trade.settings.base import *  # NOQA (ignore all errors on this line)
import sys

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1']
BASE_URL = 'http://127.0.0.1:8000'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stock_trade',
        'USER': 'stock_trade',
        'PASSWORD': 'stock_trade',
        'HOST': 'localhost',
        'PORT': 5433,
        'ATOMIC_REQUESTS': True,
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb'
    }
