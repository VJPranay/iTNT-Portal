import django_filters
from registrations.models import StartUpRegistrations,ResearcherRegistrations, StudentRegistrations,VCRegistrations, IndustryRegistrations
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datarepo.models import State,District


from django import forms
from datarepo.models import AreaOfInterest


class StartUpRegistraionsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )
    class Meta:
        model = StartUpRegistrations
        fields = ['area_of_interest', 'district', 'preferred_investment_stage']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.filters['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        else:
            self.filters['district'].queryset = District.objects.none()


class ResearcherRegistrationsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )

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
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.filters['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        else:
            self.filters['district'].queryset = District.objects.none()




class StudentRegistrationsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = StudentRegistrations
        fields = ['area_of_interest', 'district', 'department','state','institution','gender']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.filters['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        else:
            self.filters['district'].queryset = District.objects.none()


class VCRegistrationsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )
    funding_stage = django_filters.ChoiceFilter(
        choices=VCRegistrations.objects.values_list('funding_stage', 'funding_stage').distinct(),
        label='funding_stage'
    )   
        
    class Meta:
        model = VCRegistrations
        fields = ['area_of_interest', 'district','state','funding_stage','fund_type']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.filters['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        else:
            self.filters['district'].queryset = District.objects.none()


class IndustryRegistrationsFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = IndustryRegistrations
        fields = ['area_of_interest', 'industry', 'district','state']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = 'get'
        self.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        
        if 'state' in self.data:
            try:
                state_id = int(self.data.get('state'))
                self.filters['district'].queryset = District.objects.filter(state_id=state_id).order_by('name')
            except (ValueError, TypeError):
                pass
        else:
            self.filters['district'].queryset = District.objects.none()