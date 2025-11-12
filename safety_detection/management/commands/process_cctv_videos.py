from django.core.management.base import BaseCommand
from safety_detection.data_ingestion import CCTVProcessor
import os

class Command(BaseCommand):
    help = 'Process CCTV videos for anomaly detection'

    def add_arguments(self, parser):
        parser.add_argument('path', type=str, help='Path to video file or directory')
        parser.add_argument('--output-dir', type=str, help='Output directory for frames')
        parser.add_argument('--frame-interval', type=int, default=30, help='Frame processing interval')

    def handle(self, *args, **options):
        path = options['path']
        output_dir = options['output_dir']
        frame_interval = options['frame_interval']
        
        if not os.path.exists(path):
            self.stdout.write(self.style.ERROR(f"Path not found: {path}"))
            return
        
        processor = CCTVProcessor()
        
        if os.path.isfile(path):
            count = processor.process_video_file(path, output_dir=output_dir, frame_interval=frame_interval)
            self.stdout.write(self.style.SUCCESS(f"Processed {count} anomalous frames from {path}"))
        elif os.path.isdir(path):
            count = processor.process_directory(path, output_dir=output_dir)
            self.stdout.write(self.style.SUCCESS(f"Processed {count} total anomalous frames from directory"))