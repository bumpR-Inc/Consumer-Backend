release: python manage.py migrate --no-input --settings=gettingstarted.production
web: gunicorn gettingstarted.wsgi --log-file -
