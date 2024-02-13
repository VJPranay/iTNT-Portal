from django.urls import path
from .views import vc_list


urlpatterns = [
    path('vc-list', vc_list, name='vc_list')    
]