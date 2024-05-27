from django import forms
from .models import MeetingRequest
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from bootstrap_datepicker_plus.widgets import DatePickerInput, TimePickerInput

class MeetingRequestForm(forms.ModelForm):
    class Meta:
        model = MeetingRequest
        fields = ['date', 'time', 'meeting_type', 'meeting_link', 'notes']
        widgets = {
            'date': DatePickerInput(),
            'time': TimePickerInput(),
        }

    def __init__(self, *args, **kwargs):
        super(MeetingRequestForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Send Request'))
        
        
class MeetingRequestUpdateForm(forms.ModelForm):
    class Meta:
        model = MeetingRequest
        fields = ['status']

    def __init__(self, *args, **kwargs):
        super(MeetingRequestUpdateForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'post'
        self.helper.add_input(Submit('submit', 'Update Status'))