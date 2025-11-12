from django.db import models

class ThreatLevel(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'

class IncidentType(models.TextChoices):
    PROTEST = 'protest', 'Protest/Riot'
    VIOLENCE = 'violence', 'Violence'
    ACCIDENT = 'accident', 'Accident'
    NATURAL_DISASTER = 'natural_disaster', 'Natural Disaster'
    OTHER = 'other', 'Other'

class SocialMediaPost(models.Model):
    text = models.TextField()
    source = models.CharField(max_length=100)
    author = models.CharField(max_length=255, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    timestamp = models.DateTimeField()
    threat_level = models.CharField(max_length=10, choices=ThreatLevel.choices)
    incident_type = models.CharField(max_length=20, choices=IncidentType.choices)
    sentiment_score = models.FloatField(null=True, blank=True)
    confidence = models.FloatField(default=0.0)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.source} - {self.threat_level}"

    class Meta:
        ordering = ['-timestamp']

class CCTVAnalysis(models.Model):
    video_path = models.CharField(max_length=500)
    frame_image = models.ImageField(upload_to='cctv_frames/')
    timestamp = models.DateTimeField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    crowd_density = models.FloatField(null=True, blank=True)
    anomaly_detected = models.BooleanField(default=False)
    detected_objects = models.JSONField(default=dict)
    threat_level = models.CharField(max_length=10, choices=ThreatLevel.choices)
    processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"CCTV Analysis - {self.threat_level}"

class Alert(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    summary = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    threat_level = models.CharField(max_length=10, choices=ThreatLevel.choices)
    incident_type = models.CharField(max_length=20, choices=IncidentType.choices)
    sources = models.JSONField(default=list)
    confirmed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class CitizenReport(models.Model):
    description = models.TextField()
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    incident_type = models.CharField(max_length=20, choices=IncidentType.choices)
    reporter_email = models.EmailField(blank=True)
    attachments = models.FileField(upload_to='citizen_reports/', blank=True, null=True)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Citizen Report - {self.incident_type}"