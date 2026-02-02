#!/bin/bash

# =========================
# Activate virtualenv
# =========================
echo "Activating virtual environment..."
source ~/portfolior/venv/bin/activate

# =========================
# Pull latest changes from GitHub
# =========================
echo "Pulling latest code from GitHub..."
git checkout main
git pull origin main

# =========================
# Install any new dependencies
# =========================
echo "Installing requirements..."
pip install -r ~/portfolior/requirements.txt

# =========================
# Apply database migrations
# =========================
echo "Applying migrations..."
python ~/portfolior/manage.py makemigrations
python ~/portfolior/manage.py migrate

# =========================
# Collect static files
# =========================
echo "Collecting static files..."
python ~/portfolior/manage.py collectstatic --noinput

# =========================
# Restart Gunicorn
# =========================
echo "Restarting Gunicorn..."
sudo systemctl restart gunicorn

# =========================
# Restart Nginx
# =========================
echo "Restarting Nginx..."
sudo systemctl restart nginx

# =========================
# Deployment complete
# =========================
echo "Deployment finished successfully!"
