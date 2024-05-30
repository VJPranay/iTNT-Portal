import django_filters
from profiles.models import StartUp, Researcher, Student, VC, Industry,PreferredInvestmentStage
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from datarepo.models import State,District

from django import forms
from datarepo.models import AreaOfInterest

class StartUpFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )
    
    class Meta:
        model = StartUp
        fields = ['state','district','area_of_interest','year_of_establishment','fund_raised','development_stage','gender','primary_business_model','reveune_stage','dpiit_number']

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


class ResearcherFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )
    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    highest_qualification = django_filters.ChoiceFilter(
        choices=Researcher.objects.values_list('highest_qualification', 'highest_qualification').distinct(),
        label='Highest Qualification'
    )
    patent_title = django_filters.CharFilter(field_name='patents__title', lookup_expr='icontains', label='Patent Title')
    publication_title = django_filters.CharFilter(field_name='publications__title', lookup_expr='icontains', label='Publication Title')

    class Meta:
        model = Researcher
        fields = ['state', 'district', 'area_of_interest', 'department', 'institution', 'gender', 'highest_qualification', 'patent_title', 'publication_title']

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





class StudentFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )
    highest_qualification = django_filters.ChoiceFilter(
        choices=Researcher.objects.values_list('highest_qualification', 'highest_qualification').distinct(),
        label='Highest Qualification'
    )

    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],  # queryset for options
        widget=forms.Select(attrs={'class': 'form-select'})  # Specify the widget as Select
    )

    class Meta:
        model = Student
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




class VCFilter(django_filters.FilterSet):
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
        choices=[(obj.id, obj.name) for obj in PreferredInvestmentStage.objects.all()],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = VC
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


class IndustryFilter(django_filters.FilterSet):
    state = django_filters.ModelChoiceFilter(
        queryset=State.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_state'})
    )
    district = django_filters.ModelChoiceFilter(
        queryset=District.objects.none(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_district'})
    )
    area_of_interest = django_filters.ChoiceFilter(
        choices=[(obj.id, obj.name) for obj in AreaOfInterest.objects.all()],
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = Industry
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