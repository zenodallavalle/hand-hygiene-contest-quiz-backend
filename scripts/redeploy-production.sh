#!/bin/bash

git pull origin main

python manage.py migrate --settings "hand_hygiene_contest_quiz.production_settings"
python manage.py collectstatic --noinput  --settings "hand_hygiene_contest_quiz.production_settings"

sudo apache2ctl restart