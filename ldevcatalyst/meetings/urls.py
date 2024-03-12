from django.urls import path
from .views import vc_meeting_requests,fetch_startup_profiles,fetch_startup_details,vc_meeting_request,meetings,meeting,meeting_update,calendar_view,calendar_data



urlpatterns = [
    path('vc/requests', vc_meeting_requests, name='vc_meeting_requests'),
    path('vc/fetch-startup-profiles/', fetch_startup_profiles, name='vc_fetch_startup_profiles'),  
    path('vc/fetch-startup-profile/', fetch_startup_details, name='fetch_startup_details'),  
    path('startup/vc_meeting_request/', vc_meeting_request, name='startup_vc_meeting_request'),
    path('meetings/<str:meeting_status>', meetings, name='meetings'),
    path('meeting/', meeting, name='meeting'),
    path('meeting/<int:meeting_id>', meeting, name='meeting'),
    path('meeting/update/<int:meeting_id>', meeting_update, name='meeting_update'),
    path('calendar/', calendar_view, name='calendar_view'),
    path('calendar_data/', calendar_data, name='calendar_data'),
    path('calendar_data/<str:status>/', calendar_data, name='calendar_data'),
    
]