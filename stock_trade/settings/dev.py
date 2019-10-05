from stock_trade.settings.base import *  # NOQA (ignore all errors on this line)
import sys

DEBUG = True

ALLOWED_HOSTS = ['localhost', '127.0.0.1', '0.0.0.0']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stock_trade',
        'USER': 'stock_trade',
        'PASSWORD': 'stock_trade',
        'HOST': 'stock-trade_db',
        'PORT': 5432,
        'ATOMIC_REQUESTS': True,
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb'
    }

PAYSTACK_BASE_URL = env('PAYSTACK_BASE_URL', default='https://api.paystack.co/')

IEX_BASE_URL = env('IEX_BASE_URL', default='https://sandbox.iexapis.com/')
IEX_VERSION = env('IEX_VERSION', default='stable')
IEX_SECRET_TOKEN = env('IEX_SECRET_TOKEN', default='Tsk_40093c8fa3bb42218d53b4a98282836a')
