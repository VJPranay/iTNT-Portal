from django.urls import path
from .views import support_form_submit

urlpatterns = [
    path('support', support_form_submit, name='support_form_submit'),
]