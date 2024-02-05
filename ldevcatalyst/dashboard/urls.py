from django.urls import path
from .views import login,dashboard
from registrations.views import industry_registrations

urlpatterns = [
    path('', login, name='login'),
    path('index', dashboard, name='dashboard'),
    path('registraions/industry', industry_registrations, name='industry_registrations'),
]