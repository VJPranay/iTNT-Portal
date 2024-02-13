from django.urls import path
from .views import vc_meeting_requests


urlpatterns = [
    path('vc/requests', vc_meeting_requests, name='vc_meeting_requests')    
]