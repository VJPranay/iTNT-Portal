from django.urls import path
from .views import mentor_registration



urlpatterns = [
    path('mentor/', mentor_registration, name='mentor_registration'),
    
]