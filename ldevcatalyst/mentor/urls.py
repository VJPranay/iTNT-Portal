from django.urls import path
from .views import mentor_registration,mentor_approve_registration



urlpatterns = [
    path('mentor/', mentor_registration, name='mentor_registration'),
    path('mentor_approve_registration/', mentor_approve_registration, name='mentor_approve_registration'),
    
]