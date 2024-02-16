from django.urls import path
from .vc.views import vc_list,fetch_vc_profiles,fetch_vc_details


urlpatterns = [
    path('vc-list', vc_list, name='vc_list'),  
    path('vc-profiles', fetch_vc_profiles, name='fetch_vc_profiles'),
    path('vc-details', fetch_vc_details, name='fetch_vc_details')    
]