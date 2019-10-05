from stock_trade.settings.base import *  # NOQA (ignore all errors on this line)


DEBUG = False

ALLOWED_HOSTS = []
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

PAYSTACK_BASE_URL = env('PAYSTACK_BASE_URL', default='https://api.paystack.co/')

IEX_BASE_URL = env('IEX_BASE_URL', default='https://cloud.iexapis.com/')
IEX_VERSION = env('IEX_VERSION', default='stable')
IEX_SECRET_TOKEN = env('IEX_SECRET_TOKEN', default='sk_904b957e17f04298835337b1e1f15fa7')
