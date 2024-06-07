from django.contrib import admin
from .models import MeetingRequests

@admin.register(MeetingRequests)
class MeetingRequestsAdmin(admin.ModelAdmin):
    list_display = ('id','start_up', 'vc', 'message', 'created', 'updated', 'status','cancellation_reason')
    list_filter = ('status',)
