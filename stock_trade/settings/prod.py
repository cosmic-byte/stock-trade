import django_heroku

from stock_trade.settings.base import *  # NOQA (ignore all errors on this line)


DEBUG = False

ALLOWED_HOSTS = []
django_heroku.settings(locals())
BASE_URL = 'http://127.0.0.1:8000'


REDIS_URL = BROKER_URL = CELERY_RESULT_BACKEND = os.environ['REDIS_URL']
CELERY_BROKER_URL = REDIS_URL
CELERY_RESULT_SERIALIZER = 'json'
CELERY_BROKER_TRANSPORT_OPTIONS = {
    'visibility_timeout': 3600,  # 1 hour
    'fanout_prefix': True,
    'fanout_patterns': True
}

CACHES = {
    'default': {
        'BACKEND': 'django_redis.cache.RedisCache',
        'LOCATION': REDIS_URL,
        'OPTIONS': {'CLIENT_CLASS': 'django_redis.client.DefaultClient'},
    }
}