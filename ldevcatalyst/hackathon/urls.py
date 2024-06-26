from django.urls import path

from .views import hackathon_proposal_form, success_page, error_page, challenge_details



urlpatterns = [
    # Hackathon
    path('details', challenge_details, name='hackathon_challenge_details'),
    path('', hackathon_proposal_form, name='hackathon_proposal_form'),
    path('success', success_page, name='success_page'),
    path('error', error_page, name='error_page'),
]