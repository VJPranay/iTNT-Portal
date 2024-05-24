import django_filters
from registrations.models import StartUpRegistrations,ResearcherRegistrations, StudentRegistrations,VCRegistrations, IndustryRegistrations, StartUpRegistrationsCoFounders
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
    gender = django_filters.ChoiceFilter(
        field_name='startupregistartionscofounders__gender',
        choices=[('male', 'Male'), ('female', 'Female'), ('prefer not to say', 'Prefer not to say')],
        label='Gender',
    )
    
    registration_status = django_filters.ChoiceFilter(
        field_name='status',
        choices=[('pending', 'pending'), ('approved', 'approved')], # add , ('rejected', 'rejected') if they ask]
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = StartUpRegistrations
        fields = ['state','district','area_of_interest','year_of_establishment','fund_raised','gender','development_stage','primary_business_model','reveune_stage','dpiit_number']
   
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

    highest_qualification = django_filters.ChoiceFilter(
        choices=ResearcherRegistrations.objects.values_list('highest_qualification', 'highest_qualification').distinct(),
        label='Highest Qualification'
    )
    registration_status = django_filters.ChoiceFilter(
        field_name='status',
        choices=[('pending', 'pending'), ('approved', 'approved')], # add , ('rejected', 'rejected') if they ask]
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
    class Meta:
        model = ResearcherRegistrations
        fields = ['state','district','area_of_interest','department', 'institution', 'gender', 'highest_qualification', 'publications']

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

    highest_qualification = django_filters.ChoiceFilter(
        choices=ResearcherRegistrations.objects.values_list('highest_qualification', 'highest_qualification').distinct(),
        label='Highest Qualification'
    )

    class Meta:
        model = StudentRegistrations
        fields = [ 'state','district','area_of_interest','department','institution','gender','highest_qualification','paper_published']

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
        label='Funding stage'
    )   
        
    class Meta:
        model = VCRegistrations
        fields = ['state','district','area_of_interest','funding_stage','fund_type']

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
    registration_status = django_filters.ChoiceFilter(
        field_name='status',
        choices=[('pending', 'pending'), ('approved', 'approved')], # add , ('rejected', 'rejected') if they ask]
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    
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
        fields = ['state', 'district', 'industry', 'area_of_interest','state']

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