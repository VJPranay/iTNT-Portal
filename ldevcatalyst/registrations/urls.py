from django.urls import path
from .views import industry_registration

urlpatterns = [
    path('industry/', industry_registration, name='industry_registration'),
]