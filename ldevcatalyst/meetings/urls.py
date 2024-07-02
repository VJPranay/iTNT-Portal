from django.urls import path
from .views import vc_meeting_requests,fetch_startup_profiles,fetch_startup_details,vc_meeting_request,meetings,meeting,meeting_update,calendar_view,calendar_data,vc_meeting_accept,startup_confirm_meeting,startup_reject_meeting,vc_meeting_reject,meeting_details

from meetings.v2.list_view import SmeConnectListView,MentorStartupConnectListView,SmeIndustryConnectListView,VcStartup_MeetingListView
from meetings.v2.meeting_details import sme_connect_details,mentorstartup_connect_details,vcstartup_connect_details,smeindustry_connect_details



urlpatterns = [
    path('vc/requests', vc_meeting_requests, name='vc_meeting_requests'),
    path('vc/fetch-startup-profiles/', fetch_startup_profiles, name='vc_fetch_startup_profiles'),  
    path('vc/fetch-startup-profile/', fetch_startup_details, name='fetch_startup_details'),  
    path('startup/vc_meeting_request/', vc_meeting_request, name='startup_vc_meeting_request'),
    path('meetings/<str:meeting_status>', meetings, name='meetings'),
    path('meeting/', meeting, name='meeting'),
    path('meeting/<int:meeting_id>', meeting, name='meeting'),
    path('meeting/update/<int:meeting_id>', meeting_update, name='meeting_update'),
    path('meeting/accept/<int:meeting_id>', vc_meeting_accept, name='vc_meeting_accept'),
    path('meeting/reject/<int:meeting_id>', vc_meeting_reject, name='vc_meeting_reject'),
    path('calendar/', calendar_view, name='calendar_view'),
    path('calendar_data/', calendar_data, name='calendar_data'),
    path('calendar_data/<str:status>/', calendar_data, name='calendar_data'),
    path('startup_confirm_meeting',startup_confirm_meeting,name='startup_confirm_meeting'),
    path('startup_reject_meeting',startup_reject_meeting,name='startup_reject_meeting'),
    
    #meeting details
    #path('/<int:pk>/',meeting_details,name="meeting_details")
    
    
    path('meeting_details/<str:model_type>/<int:pk>/', meeting_details, name='meeting_details'),

    # V2
    path('sme_connect_list/', SmeConnectListView.as_view(), name='sme_connect_list'),
    path('sme_connect_details/<int:pk>/', sme_connect_details, name='sme_connect_details'),
    
    path('vcstartup_connect_list/', VcStartup_MeetingListView.as_view(), name='vcstartup_connect_list'),
    path('vcstartup_connect_details/<int:pk>/', vcstartup_connect_details, name='vcstartup_connect_details'),
    
    path('smeindustry_connect_list/', SmeIndustryConnectListView.as_view(), name='smeindustry_connect_list'),
    path('smeindustry_connect_details/<int:pk>/', smeindustry_connect_details, name='smeindustry_connect_details'),
    
    path('mentorstartup_connect_list/', MentorStartupConnectListView.as_view(), name='mentorstartup_connect_list'),
    path('mentorstartup_connect_details/<int:pk>/', mentorstartup_connect_details, name='mentorstartup_connect_details'),
]