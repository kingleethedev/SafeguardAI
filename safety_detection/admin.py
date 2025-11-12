from django.contrib import admin
from .models import SocialMediaPost, CCTVAnalysis, Alert, CitizenReport

@admin.register(SocialMediaPost)
class SocialMediaPostAdmin(admin.ModelAdmin):
    list_display = ['id', 'source', 'threat_level', 'incident_type', 'timestamp']
    list_filter = ['threat_level', 'incident_type', 'source']
    search_fields = ['text', 'author']

@admin.register(CCTVAnalysis)
class CCTVAnalysisAdmin(admin.ModelAdmin):
    list_display = ['id', 'threat_level', 'anomaly_detected', 'crowd_density', 'timestamp']
    list_filter = ['threat_level', 'anomaly_detected']

@admin.register(Alert)
class AlertAdmin(admin.ModelAdmin):  # Remove GISModelAdmin
    list_display = ['title', 'threat_level', 'incident_type', 'confirmed', 'created_at']
    list_filter = ['threat_level', 'incident_type', 'confirmed']

@admin.register(CitizenReport)
class CitizenReportAdmin(admin.ModelAdmin):
    list_display = ['id', 'incident_type', 'verified', 'created_at']
    list_filter = ['incident_type', 'verified']