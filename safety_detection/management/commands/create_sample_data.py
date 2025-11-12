from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random
from safety_detection.models import SocialMediaPost, CCTVAnalysis, Alert, CitizenReport

class Command(BaseCommand):
    help = 'Create sample data for Kenya demonstration'

    def handle(self, *args, **options):
        self.create_sample_social_media_posts()
        self.create_sample_cctv_analyses()
        self.create_sample_alerts()
        self.create_sample_citizen_reports()
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created sample data for Kenya demonstration')
        )

    def create_sample_social_media_posts(self):
        """Create sample social media posts with Kenya locations"""
        sample_posts = [
            {
                'text': 'Large protest forming in Nairobi CBD near Parliament. Hundreds of people gathering #protest',
                'threat_level': 'high',
                'incident_type': 'protest',
                'location': 'Nairobi CBD'
            },
            {
                'text': 'Major accident on Thika Road near Garden City. Traffic at standstill!',
                'threat_level': 'medium',
                'incident_type': 'accident',
                'location': 'Thika Road'
            },
            {
                'text': 'Fire reported in Industrial Area Nairobi. Multiple fire engines responding.',
                'threat_level': 'high',
                'incident_type': 'natural_disaster',
                'location': 'Industrial Area'
            },
            {
                'text': 'Fight broke out at Westgate Mall parking. Police called to scene.',
                'threat_level': 'medium',
                'incident_type': 'violence',
                'location': 'Westlands'
            },
            {
                'text': 'Flood warning issued for areas near Nairobi River. Water levels rising.',
                'threat_level': 'high',
                'incident_type': 'natural_disaster',
                'location': 'Nairobi River'
            },
            {
                'text': 'Suspicious activity reported at Jomo Kenyatta Airport. Security heightened.',
                'threat_level': 'high',
                'incident_type': 'violence',
                'location': 'JKIA'
            },
            {
                'text': 'Peaceful student demonstration at University of Nairobi. Everything calm.',
                'threat_level': 'low',
                'incident_type': 'protest',
                'location': 'University of Nairobi'
            },
        ]

        # Kenya coordinates (Nairobi area)
        kenya_locations = {
            'Nairobi CBD': (-1.286389, 36.817223),
            'Thika Road': (-1.2000, 36.9000),
            'Industrial Area': (-1.3167, 36.8500),
            'Westlands': (-1.2667, 36.8000),
            'Nairobi River': (-1.3000, 36.8333),
            'JKIA': (-1.3192, 36.9258),
            'University of Nairobi': (-1.2800, 36.8172),
        }

        for i, post_data in enumerate(sample_posts):
            location_name = post_data['location']
            lat, lng = kenya_locations.get(location_name, (-1.286389, 36.817223))
            
            # Add some random variation to coordinates
            lat += random.uniform(-0.01, 0.01)
            lng += random.uniform(-0.01, 0.01)
            
            SocialMediaPost.objects.create(
                text=post_data['text'],
                source='twitter',
                author=f'user_{i+1}',
                latitude=lat,
                longitude=lng,
                timestamp=timezone.now() - timedelta(hours=random.randint(1, 24)),
                threat_level=post_data['threat_level'],
                incident_type=post_data['incident_type'],
                sentiment_score=random.uniform(0.1, 0.9),
                confidence=random.uniform(0.6, 0.95)
            )

        self.stdout.write(f"Created {len(sample_posts)} sample social media posts in Kenya")

    def create_sample_cctv_analyses(self):
        """Create sample CCTV analysis results in Kenya"""
        sample_analyses = [
            {
                'location': 'Nairobi CBD',
                'crowd_density': 45,
                'threat_level': 'high',
                'detected_objects': {'people': 45, 'vehicles': 12, 'weapons': 2, 'fire': 0}
            },
            {
                'location': 'Westgate Mall',
                'crowd_density': 8,
                'threat_level': 'low',
                'detected_objects': {'people': 8, 'vehicles': 3, 'weapons': 0, 'fire': 0}
            },
            {
                'location': 'Kenyatta Avenue',
                'crowd_density': 23,
                'threat_level': 'medium',
                'detected_objects': {'people': 23, 'vehicles': 8, 'weapons': 0, 'fire': 1}
            },
            {
                'location': 'Moi Avenue',
                'crowd_density': 67,
                'threat_level': 'high',
                'detected_objects': {'people': 67, 'vehicles': 15, 'weapons': 0, 'fire': 0}
            },
        ]

        kenya_locations = {
            'Nairobi CBD': (-1.286389, 36.817223),
            'Westgate Mall': (-1.2667, 36.8000),
            'Kenyatta Avenue': (-1.2833, 36.8167),
            'Moi Avenue': (-1.2833, 36.8250),
        }

        for i, analysis_data in enumerate(sample_analyses):
            location_name = analysis_data['location']
            lat, lng = kenya_locations.get(location_name, (-1.286389, 36.817223))
            
            CCTVAnalysis.objects.create(
                video_path=f'/media/videos/kenya_sample_{i+1}.mp4',
                frame_image=f'cctv_frames/kenya_frame_{i+1}.jpg',
                timestamp=timezone.now() - timedelta(hours=random.randint(1, 12)),
                latitude=lat,
                longitude=lng,
                crowd_density=analysis_data['crowd_density'],
                anomaly_detected=analysis_data['threat_level'] != 'low',
                detected_objects=analysis_data['detected_objects'],
                threat_level=analysis_data['threat_level']
            )

        self.stdout.write(f"Created {len(sample_analyses)} sample CCTV analyses in Kenya")

    def create_sample_alerts(self):
        """Create sample alert records for Kenya"""
        sample_alerts = [
            {
                'title': 'Large Protest Detected in Nairobi CBD',
                'description': 'AI systems have detected a large gathering forming near Parliament buildings. Multiple social media posts confirm protest activity.',
                'threat_level': 'high',
                'incident_type': 'protest',
                'location': 'Nairobi CBD'
            },
            {
                'title': 'Major Traffic Accident on Thika Road',
                'description': 'Multiple vehicle collision reported with injuries. Emergency services dispatched to the scene near Garden City Mall.',
                'threat_level': 'medium',
                'incident_type': 'accident',
                'location': 'Thika Road'
            },
            {
                'title': 'Fire Emergency in Industrial Area',
                'description': 'Large fire detected in Industrial Area Nairobi. Evacuation orders being considered for nearby businesses.',
                'threat_level': 'high',
                'incident_type': 'natural_disaster',
                'location': 'Industrial Area'
            },
            {
                'title': 'Public Disturbance at Westgate Mall',
                'description': 'Altercation involving multiple individuals in parking area. Police response underway.',
                'threat_level': 'medium',
                'incident_type': 'violence',
                'location': 'Westgate Mall'
            },
        ]

        kenya_locations = {
            'Nairobi CBD': (-1.286389, 36.817223),
            'Thika Road': (-1.2000, 36.9000),
            'Industrial Area': (-1.3167, 36.8500),
            'Westgate Mall': (-1.2667, 36.8000),
        }

        for i, alert_data in enumerate(sample_alerts):
            location_name = alert_data['location']
            lat, lng = kenya_locations.get(location_name, (-1.286389, 36.817223))
            
            Alert.objects.create(
                title=alert_data['title'],
                description=alert_data['description'],
                summary=f"AI Summary: {alert_data['description'][:100]}...",
                latitude=lat,
                longitude=lng,
                threat_level=alert_data['threat_level'],
                incident_type=alert_data['incident_type'],
                sources=[f'social_media:{i*2}', f'social_media:{i*2+1}', f'cctv:{i}'],
                confirmed=random.choice([True, False])
            )

        self.stdout.write(f"Created {len(sample_alerts)} sample alerts in Kenya")

    def create_sample_citizen_reports(self):
        """Create sample citizen reports for Kenya"""
        sample_reports = [
            {
                'description': 'Saw smoke coming from building near Moi Avenue. No emergency vehicles yet.',
                'incident_type': 'natural_disaster',
                'location': 'Moi Avenue'
            },
            {
                'description': 'Group of people fighting outside KICC. Security trying to break it up.',
                'incident_type': 'violence',
                'location': 'KICC'
            },
            {
                'description': 'Matatu accident on Ngong Road. Traffic completely stopped.',
                'incident_type': 'accident',
                'location': 'Ngong Road'
            },
        ]

        for report_data in sample_reports:
            CitizenReport.objects.create(
                description=report_data['description'],
                incident_type=report_data['incident_type'],
                reporter_email='citizen@example.com',
                verified=random.choice([True, False])
            )

        self.stdout.write(f"Created {len(sample_reports)} sample citizen reports")