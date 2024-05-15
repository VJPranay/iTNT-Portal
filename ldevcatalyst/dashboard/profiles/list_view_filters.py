import django_filters
from profiles.models import StartUp, Researcher, Student, VC, Industry
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit

from django import forms
from datarepo.models import AreaOfInterest

class StartUpFilter(django_filters.FilterSet):
    class Meta:
        model = StartUp
        fields = ['area_of_interest','year_of_establishment', 'district','state','fund_raised','development_stage','gender','primary_business_model','reveune_stage','dpiit_number']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))


class ResearcherFilter(django_filters.FilterSet):
    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )
    
    highest_qualification = django_filters.ChoiceFilter(
        choices=Researcher.objects.values_list('highest_qualification', 'highest_qualification').distinct(),
        label='Highest Qualification'
    )
    
    class Meta:
        model = Researcher
        fields = ['area_of_interest', 'district', 'department', 'institution', 'gender', 'highest_qualification', 'publications']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))





class StudentFilter(django_filters.FilterSet):

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = Student
        fields = ['area_of_interest', 'district', 'department','institution','gender','year_of_graduation']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))




class VCFilter(django_filters.FilterSet):

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = VC
        fields = ['area_of_interest', 'district', 'funding_stage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))




class IndustryFilter(django_filters.FilterSet):

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = Industry
        fields = ['area_of_interest', 'district', 'industry',]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
