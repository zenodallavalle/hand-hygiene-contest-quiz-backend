#!/bin/sh

git pull origin main

python manage.py migrate
python manage.py collectstatic --noinput

sudo apache2ctl restart