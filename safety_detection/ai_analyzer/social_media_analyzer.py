import re
from transformers import pipeline

class SocialMediaAnalyzer:
    def __init__(self):
        self.sentiment_analyzer = pipeline(
            "sentiment-analysis",
            model="cardiffnlp/twitter-roberta-base-sentiment-latest"
        )
        self.threat_classifier = pipeline(
            "text-classification",
            model="cardiffnlp/twitter-roberta-base-offensive"
        )
        
        # Threat keywords with weights
        self.threat_keywords = {
            'protest': 0.3, 'riot': 0.8, 'violence': 0.7, 'attack': 0.8,
            'emergency': 0.6, 'danger': 0.5, 'fire': 0.6, 'accident': 0.5,
            'crash': 0.5, 'fight': 0.4, 'assault': 0.7, 'weapon': 0.8,
            'gun': 0.9, 'knife': 0.7, 'explosion': 0.9, 'bomb': 0.9
        }
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of social media text"""
        try:
            result = self.sentiment_analyzer(text[:512])[0]
            return result['label'], result['score']
        except Exception as e:
            print(f"Sentiment analysis error: {e}")
            return "NEUTRAL", 0.5
    
    def detect_threat(self, text):
        """Detect threat level in social media text"""
        try:
            # Get classifier result
            result = self.threat_classifier(text[:512])[0]
            text_lower = text.lower()
            
            # Base threat score from classifier
            base_score = result['score'] if result['label'] in ['offensive', 'hate'] else 0.1
            
            # Add keyword-based threat score
            keyword_score = 0
            for keyword, weight in self.threat_keywords.items():
                if keyword in text_lower:
                    keyword_score += weight
            
            # Normalize keyword score
            keyword_score = min(1.0, keyword_score * 0.3)
            
            # Combine scores
            threat_score = min(1.0, base_score + keyword_score)
            
            # Determine threat level
            if threat_score > 0.7:
                return "HIGH", threat_score
            elif threat_score > 0.4:
                return "MEDIUM", threat_score
            else:
                return "LOW", threat_score
                
        except Exception as e:
            print(f"Threat detection error: {e}")
            return "LOW", 0.1
    
    def classify_incident_type(self, text):
        """Classify the type of incident from text"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['protest', 'riot', 'march', 'demonstration']):
            return 'protest'
        elif any(word in text_lower for word in ['attack', 'violence', 'fight', 'assault', 'weapon', 'gun']):
            return 'violence'
        elif any(word in text_lower for word in ['accident', 'crash', 'collision', 'car crash']):
            return 'accident'
        elif any(word in text_lower for word in ['earthquake', 'flood', 'fire', 'disaster', 'storm']):
            return 'natural_disaster'
        else:
            return 'other'