from django.urls import path
from .industry.views import industry_registration
from .student.views import student_registration
from .vc.views import vc_registration
from .startup.views import startup_registration,fetch_startup_registrtaion_details
from .sme.views import sme_registration
urlpatterns = [
    path('industry/', industry_registration, name='industry_registration'),
    path('student/', student_registration, name='student_registration'),
    path('vc/', vc_registration, name='vc_registration'),
    path('startup/', startup_registration, name='startup_registration'),
    path('startup/details/', fetch_startup_registrtaion_details, name='startup_registrtaion_details'),
    path('sme/', sme_registration, name='sme_registration'),

]