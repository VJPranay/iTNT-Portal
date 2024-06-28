from django.contrib import admin
from .models import MentorStartupMeetingRequest
# Register your models here.

class MentorStartupMeetingRequestAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver', 'date', 'time', 'meeting_type', 'meeting_details', 'notes', 'status')

admin.site.register(MentorStartupMeetingRequest, MentorStartupMeetingRequestAdmin)
