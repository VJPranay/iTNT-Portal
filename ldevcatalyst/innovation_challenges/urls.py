from django.urls import path
from .views import create_challenge,innovation_challenges,innovation_challenge_detail

urlpatterns = [
    path('create/', create_challenge, name='ic_create_challenge'),
    path('list/<str:challenge_status>', innovation_challenges, name='innovation_challenges'),
     path('details/<int:challenge_id>/', innovation_challenge_detail, name='innovation_challenge_detail'),
    # Add other URLs as needed
]