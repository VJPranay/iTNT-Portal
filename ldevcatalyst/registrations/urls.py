from django.urls import path
from .industry.views import industry_registration,fetch_industry_registration_details
from .student.views import student_registration,fetch_student_registration_details
from .vc.views import vc_registration,vc_registration_details
from .startup.views import startup_registration,fetch_startup_registration_details
from .sme.views import sme_registration,fetch_sme_registration_details


urlpatterns = [
    path('industry/', industry_registration, name='industry_registration'),
    path('vc/', vc_registration, name='vc_registration'),
    path('startup/', startup_registration, name='startup_registration'),
    path('startup/details/', fetch_startup_registration_details, name='startup_registration_details'),
    path('vc/details/', vc_registration_details, name='vc_registration_details'),
    path('sme/', sme_registration, name='sme_registration'),
    path('industry/details/', fetch_industry_registration_details, name='industry_registration_details'),
    #student
    path('student/details/', fetch_student_registration_details, name='student_registration_details'),
    path('student/', student_registration, name='student_registration'),

    #sme
    path('sme/details/', fetch_sme_registration_details, name='sme_registration_details'),
    path('sme/', sme_registration, name='sme_registration'),



]