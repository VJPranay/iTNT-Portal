import django_filters
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from smeconnect.models import MeetingRequest



class SmeConnectFilter(django_filters.FilterSet):
    
    class Meta:
        model = MeetingRequest
        fields = ['sender', 'receiver', 'meeting_type', 'status']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        