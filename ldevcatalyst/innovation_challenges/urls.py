from django.urls import path
from .views import create_challenge,innovation_challenges,innovation_challenge_detail,submit_proposal,proposal_detail

urlpatterns = [
    path('create/', create_challenge, name='ic_create_challenge'),
    path('list/<str:challenge_status>', innovation_challenges, name='innovation_challenges'),
     path('details/<int:challenge_id>/', innovation_challenge_detail, name='innovation_challenge_detail'),
     path('submit-proposal/<int:challenge_id>', submit_proposal, name='submit_proposal'),
     path('proposal/<int:proposal_id>/', proposal_detail, name='proposal_detail'),
    # Add other URLs as needed
]