import pandas as pd
import json
from datetime import datetime
from django.utils import timezone
from ...models import SocialMediaPost
from ..ai_analyzer import SocialMediaAnalyzer

class SocialMediaIngestor:
    def __init__(self):
        self.analyzer = SocialMediaAnalyzer()
    
    def ingest_csv(self, csv_path, source='twitter'):
        """Ingest social media data from CSV file"""
        try:
            df = pd.read_csv(csv_path)
            ingested_count = 0
            
            for _, row in df.iterrows():
                try:
                    # Extract text from various possible column names
                    text = self._extract_text(row)
                    if not text or len(text.strip()) < 10:
                        continue
                    
                    # Analyze the text
                    sentiment, sentiment_score = self.analyzer.analyze_sentiment(text)
                    threat_level, confidence = self.analyzer.detect_threat(text)
                    incident_type = self.analyzer.classify_incident_type(text)
                    
                    # Create social media post
                    post = SocialMediaPost(
                        text=text[:1000],
                        source=source,
                        author=self._extract_author(row),
                        timestamp=self._extract_timestamp(row),
                        threat_level=threat_level,
                        incident_type=incident_type,
                        sentiment_score=sentiment_score,
                        confidence=confidence,
                        latitude=self._extract_latitude(row),
                        longitude=self._extract_longitude(row)
                    )
                    
                    post.save()
                    ingested_count += 1
                    
                    if ingested_count % 100 == 0:
                        print(f"Ingested {ingested_count} posts...")
                        
                except Exception as e:
                    print(f"Error processing row: {e}")
                    continue
            
            print(f"Successfully ingested {ingested_count} social media posts")
            return ingested_count
            
        except Exception as e:
            print(f"Error reading CSV file: {e}")
            return 0
    
    def _extract_text(self, row):
        """Extract text from row with multiple possible column names"""
        text_columns = ['text', 'tweet', 'content', 'message', 'post']
        
        for col in text_columns:
            if col in row and pd.notna(row[col]):
                return str(row[col])
        
        return ""
    
    def _extract_author(self, row):
        """Extract author information"""
        author_columns = ['user', 'author', 'username', 'screen_name']
        
        for col in author_columns:
            if col in row and pd.notna(row[col]):
                return str(row[col])
        
        return "unknown"
    
    def _extract_timestamp(self, row):
        """Extract timestamp from row"""
        timestamp_columns = ['timestamp', 'created_at', 'date', 'time']
        
        for col in timestamp_columns:
            if col in row and pd.notna(row[col]):
                try:
                    return pd.to_datetime(row[col])
                except:
                    pass
        
        return timezone.now()
    
    def _extract_latitude(self, row):
        """Extract latitude from row if available"""
        try:
            if 'lat' in row and pd.notna(row['lat']):
                return float(row['lat'])
            elif 'latitude' in row and pd.notna(row['latitude']):
                return float(row['latitude'])
        except:
            pass
        
        return None
    
    def _extract_longitude(self, row):
        """Extract longitude from row if available"""
        try:
            if 'lng' in row and pd.notna(row['lng']):
                return float(row['lng'])
            elif 'longitude' in row and pd.notna(row['longitude']):
                return float(row['longitude'])
            elif 'lon' in row and pd.notna(row['lon']):
                return float(row['lon'])
        except:
            pass
        
        return None