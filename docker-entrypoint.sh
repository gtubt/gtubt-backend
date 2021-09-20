#!/bin/sh

# Pass arguments to manage.py and exit (ex. makemigrations, etc)
if [ $# -gt 0 ]
  then
    python manage.py "$@"
    exit
fi

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Starting server"
python manage.py runserver 0.0.0.0:8000