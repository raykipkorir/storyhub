#! /bin/bash
set -e
set -x

cd storyhub
python3 manage.py makemigrations --no-input
python3 manage.py migrate --no-input
python3 manage.py collectstatic --no-input

gunicorn storyhub.wsgi
