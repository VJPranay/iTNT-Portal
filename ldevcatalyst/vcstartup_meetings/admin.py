from django.contrib import admin
from .models import MeetingRequest
# Register your models here.

class MeetingRequestAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver', 'date', 'time', 'meeting_type', 'meeting_details', 'notes', 'status')

admin.site.register(MeetingRequest, MeetingRequestAdmin)
