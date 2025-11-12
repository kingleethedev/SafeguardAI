#!/usr/bin/env python
import os
import sys
import django
from django.core.management import execute_from_command_line

def setup_project():
    """Setup the Django project with initial data"""
    
    # Set up Django environment
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'public_safety.settings')
    django.setup()
    
    # Create migrations and migrate
    print("Creating database migrations...")
    execute_from_command_line(['manage.py', 'makemigrations', 'safety_detection'])
    
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser (optional)
    print("\nWould you like to create a superuser? (y/n)")
    create_superuser = input().lower().strip()
    if create_superuser == 'y':
        execute_from_command_line(['manage.py', 'createsuperuser'])
    
    # Create media directories
    print("Creating media directories...")
    media_dirs = [
        'media/videos/cctv_samples',
        'media/videos/processed',
        'media/images/cctv_frames',
        'media/images/annotated_frames',
        'media/images/thumbnails',
        'media/citizen_reports/images',
        'media/citizen_reports/documents',
        'media/temp/frames',
        'media/temp/processing',
    ]
    
    for directory in media_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created: {directory}")
    
    # Create data directories
    print("Creating data directories...")
    data_dirs = [
        'data/social_media/raw',
        'data/social_media/processed',
        'data/social_media/archives',
        'data/cctv_videos/ucf_crime',
        'data/cctv_videos/ucsd_anomaly',
        'data/cctv_videos/sample_clips',
        'data/models',
        'data/exports/analytics',
    ]
    
    for directory in data_dirs:
        os.makedirs(directory, exist_ok=True)
        print(f"Created: {directory}")
    
    print("\n✅ Setup completed successfully!")
    print("\nNext steps:")
    print("1. Run: python manage.py runserver")
    print("2. Access the dashboard at: http://127.0.0.1:8000")
    print("3. Add sample data using management commands")

if __name__ == '__main__':
    setup_project()