from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views import View
from django.utils import timezone
from datetime import timedelta
from django.db.models import Count, Avg
from .models import SocialMediaPost, CCTVAnalysis, Alert, CitizenReport, ThreatLevel, IncidentType
from .forms import CitizenReportForm
from .ai_analyzer import AlertSummarizer

class DashboardView(View):
    def get(self, request):
        # Get recent alerts
        recent_alerts = Alert.objects.all().order_by('-created_at')[:10]
        
        # Get threat statistics
        threat_stats = {
            'high': Alert.objects.filter(threat_level='high').count(),
            'medium': Alert.objects.filter(threat_level='medium').count(),
            'low': Alert.objects.filter(threat_level='low').count(),
            'total': Alert.objects.count()
        }
        
        # Get recent social media posts
        recent_posts = SocialMediaPost.objects.all().order_by('-timestamp')[:5]
        
        # Get recent CCTV analyses
        recent_cctv = CCTVAnalysis.objects.filter(anomaly_detected=True).order_by('-timestamp')[:5]
        
        # Prepare data for charts
        sentiment_data = self._get_sentiment_trends()
        incident_type_data = self._get_incident_type_stats()
        
        context = {
            'recent_alerts': recent_alerts,
            'threat_stats': threat_stats,
            'recent_posts': recent_posts,
            'recent_cctv': recent_cctv,
            'sentiment_data': sentiment_data,
            'incident_type_data': incident_type_data,
        }
        
        return render(request, 'safety_detection/dashboard.html', context)
    
    def _get_sentiment_trends(self):
        """Get sentiment trends for chart"""
        return {
            'labels': ['00:00', '04:00', '08:00', '12:00', '16:00', '20:00'],
            'data': [0.6, 0.4, 0.7, 0.3, 0.8, 0.5]
        }
    
    def _get_incident_type_stats(self):
        """Get incident type statistics for chart"""
        incident_stats = Alert.objects.values('incident_type').annotate(
            count=Count('id')
        ).order_by('-count')
        
        labels = [item['incident_type'] for item in incident_stats]
        data = [item['count'] for item in incident_stats]
        
        return {
            'labels': labels,
            'data': data
        }

class AlertMapView(View):
    def get(self, request):
        alerts = Alert.objects.exclude(latitude__isnull=True).exclude(longitude__isnull=True)[:50]
        alert_data = []
        
        for alert in alerts:
            if alert.latitude and alert.longitude:
                alert_data.append({
                    'id': alert.id,
                    'title': alert.title,
                    'threat_level': alert.threat_level,
                    'lat': alert.latitude,
                    'lng': alert.longitude,
                    'type': alert.incident_type,
                    'description': alert.description[:100] + '...' if len(alert.description) > 100 else alert.description
                })
        
        return JsonResponse({'alerts': alert_data})

class CitizenReportView(View):
    def get(self, request):
        form = CitizenReportForm()
        return render(request, 'safety_detection/citizen_report.html', {'form': form})
    
    def post(self, request):
        form = CitizenReportForm(request.POST, request.FILES)
        if form.is_valid():
            report = form.save()
            
            # Create alert from citizen report
            summarizer = AlertSummarizer()
            summary = summarizer.generate_summary(
                report.incident_type, 
                {'threat_level': 'MEDIUM'}
            )
            
            alert = Alert(
                title=f"Citizen Report: {report.incident_type}",
                description=report.description,
                summary=summary,
                incident_type=report.incident_type,
                threat_level='MEDIUM',
                sources=[f'citizen_report:{report.id}']
            )
            alert.save()
            
            return redirect('report_success')
        
        return render(request, 'safety_detection/citizen_report.html', {'form': form})

class ReportSuccessView(View):
    def get(self, request):
        return render(request, 'safety_detection/report_success.html')

class SocialMediaAnalysisView(View):
    def get(self, request):
        posts = SocialMediaPost.objects.all().order_by('-timestamp')[:100]
        
        # Get statistics
        threat_levels = posts.values('threat_level').annotate(count=Count('id'))
        incident_types = posts.values('incident_type').annotate(count=Count('id'))
        
        context = {
            'posts': posts,
            'threat_levels': list(threat_levels),
            'incident_types': list(incident_types),
        }
        return render(request, 'safety_detection/social_media_analysis.html', context)

class CCTVAnalysisView(View):
    def get(self, request):
        analyses = CCTVAnalysis.objects.all().order_by('-timestamp')[:50]
        
        # Get statistics
        anomaly_stats = analyses.values('threat_level').annotate(
            count=Count('id'),
            avg_crowd=Avg('crowd_density')
        )
        
        context = {
            'analyses': analyses,
            'anomaly_stats': list(anomaly_stats),
        }
        return render(request, 'safety_detection/cctv_analysis.html', context)

class AlertsListView(View):
    def get(self, request):
        alerts = Alert.objects.all().order_by('-created_at')
        
        # Filtering
        threat_level = request.GET.get('threat_level')
        incident_type = request.GET.get('incident_type')
        
        if threat_level:
            alerts = alerts.filter(threat_level=threat_level)
        if incident_type:
            alerts = alerts.filter(incident_type=incident_type)
        
        context = {
            'alerts': alerts,
            'threat_levels': ThreatLevel.choices,
            'incident_types': IncidentType.choices,
        }
        return render(request, 'safety_detection/alerts_list.html', context)