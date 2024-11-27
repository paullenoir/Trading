#!/bin/bash
service cron start
python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic --noinput
exec python manage.py run_back "1d"