from django.urls import path
from .views import custom_login,dashboard_index,logout
from registrations.industry.views import industry_registrations,industry_approve_registration
from registrations.startup.views import startup_registrations,startup_approve_registration
from registrations.vc.views import vc_registrations,vc_approve_registration
from registrations.student.views import student_approve_registration,student_registrations
from registrations.sme.views import sme_registrations,sme_approve_registrations


urlpatterns = [
    path('', custom_login, name='login'),
    path('logout', logout, name='logout'),
    path('index', dashboard_index, name='dashboard_index'),
    path('registrations/industry/<str:registration_status>/', industry_registrations, name='industry_registrations'),
    path('registrations/startup/<str:registration_status>/', startup_registrations, name='startup_registrations'),
    path('registrations/vc/<str:registration_status>/', vc_registrations, name='vc_registrations'),
    path('registrations/industry/approve_registration', industry_approve_registration, name='industry_approve_registration'),
    path('registrations/startup/approve_registration', startup_approve_registration, name='startup_approve_registration'),
    path('registrations/vc/approve_registration', vc_approve_registration, name='vc_approve_registration'),
    #student
    path('registrations/student/<str:registration_status>/', student_registrations, name='student_registrations'),
    path('registrations/student/approve_registration', student_approve_registration, name='student_approve_registrations'),

    #sme
    path('registrations/sme/<str:registration_status>/', sme_registrations, name='sme_registrations'),
    path('registrations/sme/approve_registration', sme_approve_registrations, name='sme_approve_registrations'),
]