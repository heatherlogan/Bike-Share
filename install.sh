#!/usr/bin/env bash
cd "$(dirname "$0")"
pip3 install -r requirements.txt;
python3 manage.py migrate;
python3 manage.py createsuperuser;
python3 manage.py runserver;