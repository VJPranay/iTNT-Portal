from django.urls import path
from .views import custom_login,dashboard_index,logout
from registrations.industry.views import industry_registrations,approve_registration


urlpatterns = [
    path('', custom_login, name='login'),
    path('logout', logout, name='logout'),
    path('index', dashboard_index, name='dashboard_index'),
    path('registraions/industry/<str:registraion_status>', industry_registrations, name='industry_registrations'),
    path('registraions/industry/approve_registration/', approve_registration, name='industry_approve_registration'),
]