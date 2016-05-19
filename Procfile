web: gunicorn wdwe.wsgi --log-file -
worker: celery -A wdwe.celery worker --loglevel=info