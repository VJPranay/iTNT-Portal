from django.urls import path
from .views import industry_registration,approve_registration

urlpatterns = [
    path('industry/', industry_registration, name='industry_registration'),
    path('registraions/industry/pending/approve_registration/<int:registration_id>/', approve_registration, name='approve_registration'),
]