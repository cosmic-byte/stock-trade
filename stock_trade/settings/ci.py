from stock_trade.settings.dev import *  # NOQA (ignore all errors on this line)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'testdb'
    }
}
