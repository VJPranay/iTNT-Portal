from django.urls import path
from .vc.views import vc_list,fetch_vc_profiles,fetch_vc_details
from .student.views import student_list,fetch_student_profiles,fetch_student_details
from .sme.views import sme_list,fetch_sme_profiles,fetch_sme_details
from .industry.views import industry_list,fetch_industry_profiles,fetch_industry_details
from .startup.views import startup_list,fetch_startup_profiles,fetch_startup_details


urlpatterns = [
    path('vc-list', vc_list, name='vc_list'),  
    path('vc-profiles', fetch_vc_profiles, name='fetch_vc_profiles'),
    path('vc-details', fetch_vc_details, name='fetch_vc_details') ,

    #student
    path('student-list', student_list, name='student_list'),  
    path('student-profiles',fetch_student_profiles , name='fetch_student_profiles'),
    path('student-details', fetch_student_details, name='fetch_student_details') ,

    #sme
    path('sme-list', sme_list, name='sme_list'),  
    path('sme-profiles', fetch_sme_profiles, name='fetch_sme_profiles'),
    path('sme-details', fetch_sme_details, name='fetch_sme_details') ,

    #industry
    path('industry-list', industry_list, name='industry_list'),  
    path('industry-profiles', fetch_industry_profiles, name='fetch_industry_profiles'),
    path('industry-details', fetch_industry_details, name='fetch_industry_details') ,

    #startup
    path('startup-list', startup_list, name='startup_list'),  
    path('startup-profiles', fetch_startup_profiles, name='fetch_startup_profiles'),
    path('startup-details', fetch_startup_details, name='fetch_startup_details') ,
    

]
