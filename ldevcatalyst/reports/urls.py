from django.urls import path
from .startup.views import startup_overview
from .sme.views import researcher_overview  
from .meetings.views import meeting_counts


urlpatterns = [
    path('startup_overview', startup_overview, name='startup_overview'),
    path('researcher_overview', researcher_overview, name='researcher_overview'),
    path('meeting-overview', meeting_counts, name='meeting_counts'),
]