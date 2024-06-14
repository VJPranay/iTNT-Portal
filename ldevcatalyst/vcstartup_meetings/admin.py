from django.contrib import admin
from .models import vcstartup_MeetingRequest
# Register your models here.

class vcstartup_MeetingRequestAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver', 'date', 'time', 'meeting_type', 'meeting_details', 'notes', 'status')

admin.site.register(vcstartup_MeetingRequest, vcstartup_MeetingRequestAdmin)
