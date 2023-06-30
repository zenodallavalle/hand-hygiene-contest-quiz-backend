#!/bin/sh



cd /var/www/vhosts/hand-hygiene-contest-quiz-backend
. env/bin/activate

ssh-keyscan github.com >> ~/.ssh/known_hosts
git pull origin main

python manage.py migrate --settings "hand_hygiene_contest_backend.production_settings"
python manage.py collectstatic --noinput  --settings "hand_hygiene_contest_backend.production_settings"

sudo apache2ctl restart

deactivate