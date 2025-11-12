from django.core.management.base import BaseCommand
from safety_detection.data_ingestion import SocialMediaIngestor
import os

class Command(BaseCommand):
    help = 'Ingest social media data from CSV or JSON files'

    def add_arguments(self, parser):
        parser.add_argument('file_path', type=str, help='Path to the data file')
        parser.add_argument('--source', type=str, default='twitter', help='Data source (twitter, facebook, etc.)')

    def handle(self, *args, **options):
        file_path = options['file_path']
        source = options['source']
        
        if not os.path.exists(file_path):
            self.stdout.write(self.style.ERROR(f"File not found: {file_path}"))
            return
        
        ingestor = SocialMediaIngestor()
        
        if file_path.endswith('.csv'):
            count = ingestor.ingest_csv(file_path, source)
        elif file_path.endswith('.json'):
            count = ingestor.ingest_json(file_path, source)
        else:
            self.stdout.write(self.style.ERROR("Unsupported file format. Use CSV or JSON."))
            return
        
        if count > 0:
            self.stdout.write(self.style.SUCCESS(f"Successfully ingested {count} social media posts"))
        else:
            self.stdout.write(self.style.WARNING("No posts were ingested"))