from django.contrib import admin
from .models import MeetingRequests

@admin.register(MeetingRequests)
class MeetingRequestsAdmin(admin.ModelAdmin):
    list_display = ('start_up', 'vc', 'message', 'created', 'updated', 'status')
    list_filter = ('status',)
