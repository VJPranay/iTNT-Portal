from django.urls import path
from .views import vc_meeting_requests,fetch_startup_profiles,fetch_startup_details,vc_meeting_request,student_meeting_request,fetch_student_profiles,fetch_student_details



urlpatterns = [
    path('vc/requests', vc_meeting_requests, name='vc_meeting_requests'),
    path('vc/fetch-startup-profiles/', fetch_startup_profiles, name='vc_fetch_startup_profiles'),  
    path('vc/fetch-startup-profile/', fetch_startup_details, name='fetch_startup_details'),  
    path('startup/vc_meeting_request/', vc_meeting_request, name='startup_vc_meeting_request'),
    #student
    path('student/vc_meeting_request/', student_meeting_request, name='industry_student_meeting_request'),  
    path('student/fetch-student-profiles/',  fetch_student_profiles, name='industry_fetch_student_profiles'),  
    path('student/fetch-student-profile/', fetch_student_details, name='fetch_student_details'), 
]