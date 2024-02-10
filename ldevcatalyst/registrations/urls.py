from django.urls import path
from .industry.views import industry_registration
from .vc.views import vc_registration
from .student.views import student_registration
from .startup.views import startup_registration
urlpatterns = [
    path('industry/', industry_registration, name='industry_registration'),
    path('student/', student_registration, name='student_registration'),
    path('vc/', vc_registration, name='vc_registration'),
    path('startup/', startup_registration, name='startup_registration'),

]