#!/bin/bash

python manage.py migrate
python manage.py collectstatic --no-input
python manage.py import_ingredients

exec "$@"