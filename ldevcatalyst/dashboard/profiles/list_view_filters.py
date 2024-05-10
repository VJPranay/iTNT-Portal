import django_filters
from profiles.models import StartUp
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

class StartUpFilter(django_filters.FilterSet):
    class Meta:
        model = StartUp
        fields = ['area_of_interest', 'district', 'year_of_establishment']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
