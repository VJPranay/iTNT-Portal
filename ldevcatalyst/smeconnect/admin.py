from django.contrib import admin
from .models import MeetingRequest

class MeetingRequestAdmin(admin.ModelAdmin):
    list_display = ('id','sender','receiver','date','time','meeting_type','meeting_link','notes','status')
    
admin.site.register(MeetingRequest, MeetingRequestAdmin)

