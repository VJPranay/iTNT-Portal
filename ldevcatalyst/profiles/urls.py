from django.urls import path
from .vc.views import vc_list,fetch_vc_profiles,fetch_vc_details
from .student.views import student_list,fetch_student_profiles,fetch_student_details


urlpatterns = [
    path('vc-list', vc_list, name='vc_list'),  
    path('vc-profiles', fetch_vc_profiles, name='fetch_vc_profiles'),
    path('vc-details', fetch_vc_details, name='fetch_vc_details') ,

    #student
    path('student-list', student_list, name='student_list'),  
    path('student-profiles',fetch_student_profiles , name='fetch_student_profiles'),
    path('student-details', fetch_student_details, name='fetch_student_details') 

       
]