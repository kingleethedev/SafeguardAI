#!/bin/bash
# setup.sh

# Create virtual environment
python -m venv venv
source  venv\Scripts\activate

# Install requirements
pip install -r requirements.txt

# Run migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Download YOLO model
python -c "from ultralytics import YOLO; YOLO('yolov8n.pt')"

echo "Setup complete! Run with: python manage.py runserver"