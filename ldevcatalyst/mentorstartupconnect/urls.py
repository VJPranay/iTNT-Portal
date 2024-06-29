from django.urls import path
from .import views

urlpatterns = [
    path('mentorstartup/', views.mentorstartup_meeting_request_list, name='mentorstartup_meeting_request_list'),
    path('confirmed', views.mentorstartup_confirmed_meeting_request_list, name='mentorstartup_confirmed_meeting_request_list'),
    path('<int:pk>/', views.mentorstartup_meeting_request_detail, name='mentorstartup_meeting_request_detail'),
    path('create/<int:receiver_id>', views.mentorstartup_meeting_request_create, name='mentorstartup_meeting_request_create'),
    path('<int:pk>/update/', views.mentorstartup_meeting_request_update, name='mentorstartup_meeting_request_update'),
    path('<int:pk>/cancel/', views.mentorstartup_meeting_request_cancel, name='mentorstartup_meeting_request_cancel'),
    path('<int:pk>/accept/', views.mentorstartup_meeting_request_accept, name='mentorstartup_meeting_request_accept'),
    path('<int:pk>/reject/', views.mentorstartup_meeting_request_reject, name='mentorstartup_meeting_request_reject'),
    path('calendar/', views.mentorstartup_calendar_view, name='mentorstartup_calendar_view'),
    path('mentorstartup_calendar_data/', views.mentorstartup_calendar_data, name='mentorstartup_calendar_data'),
    path('calendar_data/<str:status>/', views.mentorstartup_calendar_data, name='calendar_data'),
 ]
