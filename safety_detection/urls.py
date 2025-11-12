from django.urls import path
from . import views

urlpatterns = [
    path('', views.DashboardView.as_view(), name='dashboard'),
    path('api/alerts/', views.AlertMapView.as_view(), name='alert_map'),
    path('report/', views.CitizenReportView.as_view(), name='citizen_report'),
    path('report/success/', views.ReportSuccessView.as_view(), name='report_success'),
    path('social-media/', views.SocialMediaAnalysisView.as_view(), name='social_media'),
    path('cctv/', views.CCTVAnalysisView.as_view(), name='cctv_analysis'),
    path('alerts/', views.AlertsListView.as_view(), name='alerts_list'),
]