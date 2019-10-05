#!/usr/bin/env bash

# Script to run the Django server in a development environment

pip install -e .

python manage.py migrate
python manage.py runserver 0.0.0.0:8081
