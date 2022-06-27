#!/bin/bash
rm -rf db.sqlite3
python ./dashboard/manage.py makemigrations
python ./dashboard/manage.py migrate
