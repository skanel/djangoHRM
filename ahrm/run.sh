#!/bin/sh
export DJANGO_SETTINGS_MODULE=settings
export PYTHONPATH=$PYTHONPATH:$DJANGOPATH

echo "Welcome to ALLWEB Human Resource Management"
echo "***** Starting the server *****"
python manage.py runserver 8282
