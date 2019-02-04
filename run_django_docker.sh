#!/usr/bin/env bash
echo ===== INSTALLING PYTHON DEPENDENCIES =====
cd /srv
pip install -r requirements.txt
echo ===== RUN DATABASE MIGRATION =====
python manage.py makemigrations
python manage.py migrate
echo ===== RUN PYTHON SERVER =====
python manage.py runserver 0.0.0.0:8000
