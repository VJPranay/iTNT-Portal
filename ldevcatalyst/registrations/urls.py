from django.urls import path
from .industry.views import industry_registration,approve_registration

urlpatterns = [
    path('industry/', industry_registration, name='industry_registration'),

]