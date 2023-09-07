#!/bin/sh

cd /var/www/vhosts/hand-hygiene-contest-quiz-backend

git pull origin main

. env/bin/activate
pip install -r requirements.txt

python manage.py migrate --settings "hand_hygiene_contest_backend.production_settings"
python manage.py collectstatic --noinput  --settings "hand_hygiene_contest_backend.production_settings"

sudo apache2ctl restart

deactivate