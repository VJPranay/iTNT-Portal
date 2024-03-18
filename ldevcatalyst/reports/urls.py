from django.urls import path
from .startup.views import startup_overview


urlpatterns = [
    path('startup_overview', startup_overview, name='startup_overview'),
]