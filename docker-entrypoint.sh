#!/bin/sh

# Apply database migrations
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Sending startup command"
exec "$@"