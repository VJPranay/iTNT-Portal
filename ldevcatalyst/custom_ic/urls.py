from django.urls import path
from .rolls_royce.views import challenge_details, proposal_form


urlpatterns = [
    path('details', challenge_details, name='rolls_royce_challenge_details'),
    path('submit-proposal', proposal_form, name='rolls_royce_proposal_form'),
]