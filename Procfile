release: python manage.py migrate
web: gunicorn portal.wsgi
worker: celery worker -A portal -B -l info -E --concurrency=10