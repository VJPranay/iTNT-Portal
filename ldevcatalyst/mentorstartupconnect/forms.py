from django import forms
from .models import MentorStartupMeetingRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput
from datetime import datetime

class MeetingRequestForm(forms.ModelForm):
    class Meta:
        model = MentorStartupMeetingRequest
        fields = ['date', 'time', 'meeting_type', 'meeting_details', 'notes']
        widgets = {
            'date': DatePickerInput(options={
                'format': 'YYYY-MM-DD',
                'minDate': datetime.now().strftime('%Y-%m-%d'),
            }),
            'time': TimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super(MeetingRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Request'))
        
        
class MeetingRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = MentorStartupMeetingRequest
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(MeetingRequestUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update Status'))
        
        
class MeetingRequestCancelForm(forms.ModelForm):
    class Meta:
        model = MentorStartupMeetingRequest
        fields = ['notes']

    def __init__(self, *args, **kwargs):
        super(MeetingRequestCancelForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Cancel Meeting'))