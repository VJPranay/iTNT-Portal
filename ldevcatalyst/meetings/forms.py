from django import forms
from .models import MeetingRequests

class MeetingRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = MeetingRequests
        fields = ['meeting_date', 'meeting_time', 'meeting_type', 'message', 'meeting_location']

    def __init__(self, *args, user_role=None, **kwargs):
        super(MeetingRequestUpdateForm, self).__init__(*args, **kwargs)
        
        # If user_role is 8, restrict fields
        if user_role == 8:
            self.fields.pop('meeting_location')
        
        # If meeting_type is offline, restrict fields
        if self.instance.meeting_type == 'offline':
            self.fields.pop('meeting_date')
            self.fields.pop('meeting_time')
            self.fields.pop('meeting_type')
            self.fields.pop('message')
        elif user_role == 8:
            # If user_role is 8, limit fields
            self.fields.pop('meeting_date')
            self.fields.pop('meeting_time')
            self.fields.pop('meeting_type')
            self.fields.pop('message')

        # If user_role is 6, allow all fields
        elif user_role == 6:
            pass
