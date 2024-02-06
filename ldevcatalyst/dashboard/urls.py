from django.urls import path
from .views import custom_login,dashboard_index,logout
from registrations.views import industry_registrations


urlpatterns = [
    path('', custom_login, name='login'),
    path('logout', logout, name='logout'),
    path('index', dashboard_index, name='dashboard_index'),
    path('registraions/industry', industry_registrations, name='industry_registrations'),
]