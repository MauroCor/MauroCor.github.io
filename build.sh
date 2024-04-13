#!/usr/bin/env bash
# Exit on error
set -o errexit

# mkvirtualenv --python=/usr/bin/python3.10 venv
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py makemigrations
python manage.py migrate