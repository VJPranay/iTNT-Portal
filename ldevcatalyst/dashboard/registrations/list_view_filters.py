import django_filters
from registrations.models import StartUpRegistrations,ResearcherRegistrations, StudentRegistrations,VCRegistrations, IndustryRegistrations
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


from django import forms
from datarepo.models import AreaOfInterest


class StartUpRegistraionsFilter(django_filters.FilterSet):
    class Meta:
        model = StartUpRegistrations
        fields = ['area_of_interest', 'district', 'preferred_investment_stage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))


class ResearcherRegistrationsFilter(django_filters.FilterSet):

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )
    
    class Meta:
        model = ResearcherRegistrations
        fields = ['area_of_interest', 'district', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))




class StudentRegistrationsFilter(django_filters.FilterSet):

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = StudentRegistrations
        fields = ['area_of_interest', 'district', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))


class VCRegistrationsFilter(django_filters.FilterSet):

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )
    class Meta:
        model = VCRegistrations
        fields = ['area_of_interest', 'district']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))


class IndustryRegistrationsFilter(django_filters.FilterSet):

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = IndustryRegistrations
        fields = ['area_of_interest', 'industry', 'district']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))