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
    path('calendar/', views.vcstartup_calendar_view, name='vcstartup_calendar_view'),
    path('vcstartup_calendar_data/', views.vcstartup_calendar_data, name='vcstartup_calendar_data'),
    path('calendar_data/<str:status>/', views.vcstartup_calendar_data, name='calendar_data'),
 ]
