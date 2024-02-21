#!/bin/sh
set -e
set -x

cd storyhub

python manage.py migrate --no-input
python manage.py collectstatic --no-input

gunicorn --threads 3 -b 0.0.0.0:8000 storyhub.wsgi
