#!/usr/bin/env bash

# Script to run the Django server in a development environment

python manage.py migrate
python manage.py runserver 0.0.0.0:8001
