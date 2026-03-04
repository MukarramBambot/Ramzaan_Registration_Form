#!/bin/bash
set -e

PROJECT_DIR="/var/www/Ramzaan_Registration_Form/backend"
VENV_PYTHON="$PROJECT_DIR/venv/bin/python3"

cd "$PROJECT_DIR"

echo "----------------------------------------"
echo "Starting Deployment at $(date)"
echo "----------------------------------------"

echo "1. Applying Database Migrations..."
$VENV_PYTHON manage.py migrate --noinput

echo "2. Restarting Gunicorn (Backend)..."
sudo systemctl restart sherullah-backend.service

echo "3. Restarting Celery..."
sudo systemctl restart sherullah-celery.service

echo "----------------------------------------"
echo "Deployment actions completed successfully."
echo "----------------------------------------"
