#!/usr/bin/env bash
# Exit on error
set -o errexit

# mkvirtualenv --python=/usr/bin/python3.10 venv
pip install -r requirements.txt

python manage.py makemigrations
python manage.py migrate