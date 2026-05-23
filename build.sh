#!/usr/bin/env bash
# exit on error
set -o errexit

# Install Python packages
pip install -r requirements.txt

# Collect static files
python manage.py collectstatic --no-input

# Run migrations
python manage.py migrate

# Seed initial database records (Idempotent)
python create_admin.py
python populate_dummy_data.py
