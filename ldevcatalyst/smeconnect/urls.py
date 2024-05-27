from django.urls import path
from . import views

urlpatterns = [
    path('', views.meeting_request_list, name='meeting_request_list'),
    path('confirmed', views.confirmed_meeting_request_list, name='confirmed_meeting_request_list'),
    path('<int:pk>/', views.meeting_request_detail, name='meeting_request_detail'),
    path('create/<int:receiver_id>', views.meeting_request_create, name='meeting_request_create'),
    path('<int:pk>/update/', views.meeting_request_update, name='meeting_request_update'),
    path('<int:pk>/accept/', views.meeting_request_accept, name='meeting_request_accept'),
    path('<int:pk>/reject/', views.meeting_request_reject, name='meeting_request_reject'),
]