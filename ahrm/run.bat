@echo off

set DJANGO_SETTINGS_MODULE=settings

set PYTHONPATH=%PYTHONPATH%;%DJANGO_PATH%;%CD%;
echo Welcome to ALLWEB Human Resource Management

echo ***** Starting the server *****
title AHRM Application 
python manage.py runserver 8282

