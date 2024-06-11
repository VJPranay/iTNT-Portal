from django.urls import path
from .import views

urlpatterns = [
    path('vcstartup/', views.vcstartup_meeting_request_list, name='vcstartup_meeting_request_list'),
    path('confirmed', views.vcstartup_confirmed_meeting_request_list, name='vcstartup_confirmed_meeting_request_list'),
    path('<int:pk>/', views.vcstartup_meeting_request_detail, name='vcstartup_meeting_request_detail'),
    path('create/<int:receiver_id>', views.vcstartup_meeting_request_create, name='vcstartup_meeting_request_create'),
    path('<int:pk>/update/', views.vcstartup_meeting_request_update, name='vcstartup_meeting_request_update'),
    path('<int:pk>/cancel/', views.vcstartup_meeting_request_cancel, name='vcstartup_meeting_request_cancel'),
    path('<int:pk>/accept/', views.vcstartup_meeting_request_accept, name='vcstartup_meeting_request_accept'),
    path('<int:pk>/reject/', views.vcstartup_meeting_request_reject, name='vcstartup_meeting_request_reject'),
]
