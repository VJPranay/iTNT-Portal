from django.urls import path
from .import views

urlpatterns = [
    path('smeindustry/', views.smeindustry_meeting_request_list, name='smeindustry_meeting_request_list'),
    path('confirmed', views.smeindustry_confirmed_meeting_request_list, name='smeindustry_confirmed_meeting_request_list'),
    path('<int:pk>/', views.smeindustry_meeting_request_detail, name='smeindustry_meeting_request_detail'),
    path('create/<int:receiver_id>', views.smeindustry_meeting_request_create, name='smeindustry_meeting_request_create'),
    path('<int:pk>/update/', views.smeindustry_meeting_request_update, name='smeindustry_meeting_request_update'),
    path('<int:pk>/cancel/', views.smeindustry_meeting_request_cancel, name='smeindustry_meeting_request_cancel'),
    path('<int:pk>/accept/', views.smeindustry_meeting_request_accept, name='smeindustry_meeting_request_accept'),
    path('<int:pk>/reject/', views.smeindustry_meeting_request_reject, name='smeindustry_meeting_request_reject'),
    path('calendar/', views.smeindustry_calendar_view, name='smeindustry_calendar_view'),
    path('smeindustry_calendar_data/', views.smeindustry_calendar_data, name='smeindustry_calendar_data'),
    path('calendar_data/<str:status>/', views.smeindustry_calendar_data, name='smeindustry_calendar_data'),
    
]