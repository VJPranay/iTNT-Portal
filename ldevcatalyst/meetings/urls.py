from django.urls import path
from .views import vc_meeting_requests,fetch_startup_profiles,fetch_startup_details



urlpatterns = [
    path('vc/requests', vc_meeting_requests, name='vc_meeting_requests'),
    path('vc/fetch-startup-profiles/', fetch_startup_profiles, name='vc_fetch_startup_profiles'),  
    path('vc/fetch-startup-profile/', fetch_startup_details, name='fetch_startup_details'),  
]