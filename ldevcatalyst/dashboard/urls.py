from django.urls import path
from .views import custom_login,dashboard_index,logout
from registrations.industry.views import industry_registrations,industry_approve_registration
from registrations.startup.views import startup_registrations,startup_approve_registration
from registrations.vc.views import vc_registrations,vc_approve_registration


urlpatterns = [
    path('', custom_login, name='login'),
    path('logout', logout, name='logout'),
    path('index', dashboard_index, name='dashboard_index'),
    #path('registrations/industry/<str:registration_status>/', industry_registrations, name='industry_registrations'),
    path('registrations/startup/<str:registration_status>/', startup_registrations, name='startup_registrations'),
    path('registrations/vc/<str:registration_status>/', vc_registrations, name='vc_registrations'),
    #path('registrations/industry/approve_registration', industry_approve_registration, name='industry_approve_registration'),
    path('registrations/startup/approve_registration', startup_approve_registration, name='startup_approve_registration'),
    path('registrations/vc/approve_registration', vc_approve_registration, name='vc_approve_registration'),
]