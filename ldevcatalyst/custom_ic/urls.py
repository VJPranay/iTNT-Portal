from django.urls import path
from .rolls_royce.views import challenge_details, proposal_form, error_page, success_page


urlpatterns = [
    path('details', challenge_details, name='rolls_royce_challenge_details'),
    path('submit-proposal', proposal_form, name='rolls_royce_proposal_form'),
    path('success', success_page, name='rolls_royce_success_page'),
    path('error', error_page, name='rolls_royce_error_page'),
]