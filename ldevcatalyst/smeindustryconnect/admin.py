from django.contrib import admin
from .models import SmeIndustryMeetingRequest
# Register your models here.

class SmeIndustryMeetingRequestAdmin(admin.ModelAdmin):
    list_display = ('id','sender', 'receiver', 'date', 'time', 'meeting_type', 'meeting_details', 'notes', 'status')

admin.site.register(SmeIndustryMeetingRequest, SmeIndustryMeetingRequestAdmin)
