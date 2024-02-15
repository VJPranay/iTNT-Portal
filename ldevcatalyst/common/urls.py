from django.urls import path
from .views import not_found


urlpatterns = [
    path('not_found', not_found, name='not_found')    
]