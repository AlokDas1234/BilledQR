from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='views_template_urls'),
    path('process-scan/', views.process_scan, name='process_scan'),
    path('process-final-scan/', views.process_final_scan, name='process_final_scan'),
]
