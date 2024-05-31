from django.urls import path
from .startup.views import startup_overview
from .sme.views import researcher_overview  
from .meetings.views import meeting_counts
from .vc.views import vc_overview
from .student.views import student_overview
from .industry.views import industry_overview


urlpatterns = [
    path('startup_overview', startup_overview, name='startup_overview'),
    path('researcher_overview', researcher_overview, name='researcher_overview'),
    path('meeting-overview', meeting_counts, name='meeting_counts'),
    path('vc_overview', vc_overview, name='vc_overview'),
    path('student_overview', student_overview, name='student_overview'),
    path('industry_overview', industry_overview, name='industry_overview'),
]