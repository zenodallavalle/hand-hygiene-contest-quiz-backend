#!/bin/sh

git pull origin main

python manage.py migrate
python manage.py collectstatic --noinput
