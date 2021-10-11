#!/bin/sh

# Apply database migrations, This step might be optional
echo "Apply database migrations"
python manage.py migrate

# Start server
echo "Sending startup command"
exec "$@"
