import random

class AlertSummarizer:
    def __init__(self):
        self.summary_templates = {
            'protest': [
                "Protest activity detected with approximately {crowd_size} people. Threat level: {threat_level}.",
                "Crowd gathering identified as potential protest. Estimated {crowd_size} participants. {threat_level} threat.",
                "Public demonstration ongoing with {crowd_size} individuals. Monitoring recommended."
            ],
            'violence': [
                "Violent activity detected with weapons present. Immediate attention required. Threat level: {threat_level}.",
                "Physical altercation or violent behavior observed. {threat_level} threat level.",
                "Weapon-related incident reported. Law enforcement response recommended."
            ],
            'accident': [
                "Traffic accident detected involving multiple vehicles. Emergency services notified. Threat level: {threat_level}.",
                "Road incident reported with potential injuries. {threat_level} threat level.",
                "Vehicle collision observed. Medical assistance may be required."
            ],
            'natural_disaster': [
                "Potential natural disaster situation unfolding. Threat level: {threat_level}.",
                "Emergency situation detected consistent with natural disaster. {threat_level} threat.",
                "Environmental hazard or disaster conditions observed."
            ],
            'other': [
                "Unusual activity detected in monitored area. Threat level: {threat_level}.",
                "Suspicious behavior or anomaly observed. {threat_level} threat level.",
                "Potential security concern identified in area."
            ]
        }
    
    def generate_summary(self, incident_type, data):
        """Generate alert summary based on incident type and data"""
        templates = self.summary_templates.get(incident_type, self.summary_templates['other'])
        template = random.choice(templates)
        
        # Fill template with data
        summary = template.format(
            crowd_size=data.get('crowd_size', 'multiple'),
            threat_level=data.get('threat_level', 'unknown')
        )
        
        return summary
    
    def generate_detailed_alert(self, social_posts, cctv_analyses, incident_type):
        """Generate detailed alert combining multiple data sources"""
        base_summary = self.generate_summary(incident_type, {
            'crowd_size': self._estimate_crowd_size(cctv_analyses),
            'threat_level': self._calculate_combined_threat(social_posts, cctv_analyses)
        })
        
        # Add supporting details
        details = []
        
        if social_posts:
            details.append(f"Supported by {len(social_posts)} social media reports.")
        
        if cctv_analyses:
            details.append(f"Confirmed by {len(cctv_analyses)} CCTV detections.")
        
        if details:
            base_summary += " " + " ".join(details)
        
        return base_summary
    
    def _estimate_crowd_size(self, cctv_analyses):
        """Estimate crowd size from CCTV analyses"""
        if not cctv_analyses:
            return "unknown number of"
        
        max_crowd = max(analysis.get('crowd_density', 0) for analysis in cctv_analyses)
        
        if max_crowd > 100:
            return "large crowd of"
        elif max_crowd > 50:
            return "medium-sized crowd of"
        elif max_crowd > 10:
            return "small group of"
        else:
            return "few"
    
    def _calculate_combined_threat(self, social_posts, cctv_analyses):
        """Calculate combined threat level from multiple sources"""
        threat_scores = []
        
        # Add social media threat scores
        for post in social_posts:
            if hasattr(post, 'confidence'):
                threat_score = post.confidence
                if post.threat_level == 'HIGH':
                    threat_score *= 1.5
                elif post.threat_level == 'MEDIUM':
                    threat_score *= 1.2
                threat_scores.append(threat_score)
        
        # Add CCTV threat scores
        for analysis in cctv_analyses:
            threat_score = analysis.get('threat_score', 0)
            threat_scores.append(threat_score)
        
        if not threat_scores:
            return "LOW"
        
        avg_threat = sum(threat_scores) / len(threat_scores)
        
        if avg_threat > 1.0:
            return "HIGH"
        elif avg_threat > 0.5:
            return "MEDIUM"
        else:
            return "LOW"