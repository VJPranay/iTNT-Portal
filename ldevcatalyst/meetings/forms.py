from django import forms
from .models import MeetingRequests

class MeetingRequestUpdateForm(forms.ModelForm):

    widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    class Meta:
        model = MeetingRequests
        exclude = ['start_up', 'vc', 'meeting_date_time']


class VCMeetingRequestAcceptForm(forms.ModelForm):

    widgets = {
            'meeting_date': forms.DateInput(attrs={'type': 'date'}),
            'meeting_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    class Meta:
        model = MeetingRequests
        exclude = ['start_up', 'vc', 'meeting_date_time','status','created','updated','']

