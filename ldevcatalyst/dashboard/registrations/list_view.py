from django.views.generic import ListView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.db.models import Q
from registrations.models import StartUpRegistrations,ResearcherRegistrations, StudentRegistrations,VCRegistrations, IndustryRegistrations
from .list_view_filters import StartUpRegistraionsFilter, ResearcherRegistrationsFilter, StudentRegistrationsFilter,VCRegistrationsFilter, IndustryRegistrationsFilter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required



class StartUpRegistrationsListView(FilterView):
    model = StartUpRegistrations
    template_name = 'dashboard/registrations/v2/startup_registrations_list.html'
    filterset_class = StartUpRegistraionsFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'company_name':
            queryset = queryset.order_by('company_name')
        elif sort_by == 'year_of_establishment':
            queryset = queryset.order_by('year_of_establishment')
        elif sort_by == 'team_size':
            queryset == queryset.order_by('team_size')
        elif sort_by =='funding_request_amount':
            queryset == queryset.order_by('funding_request_amount')
        else:
            queryset = queryset.order_by('-id')

            

        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        year_of_establishment=self.request.GET.get('year_of_establishment')
        district = self.request.GET.get('district')
        state=self.request.GET.get('state')
        fund_raised=self.request.GET.get('fund_raised')
        development_stage=self.request.GET.get('development_stage') 
        primary_business_model=self.request.GET.get('primary_business_model')
        reveune_stage=self.request.GET.get('reveune_stage')
        dpiit_number=self.request.GET.get('dpiit_number')
        gender = self.request.GET.get('gender')

        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if year_of_establishment:
            filters &= Q(year_of_establishment=year_of_establishment)
        if district:
            filters &= Q(district=district)
        if  state:
            filters &= Q(state=state)
        if fund_raised:
            filters &= Q(fund_raised=fund_raised)
        if development_stage:
            filters &= Q(development_stage=development_stage)   
        if  primary_business_model:
            filters &= Q( primary_business_model= primary_business_model)
        if  reveune_stage:
            filters &= Q( reveune_stage= reveune_stage)
        if   dpiit_number:
            filters &= Q(  dpiit_number=dpiit_number)

        if gender:
            filters &= Q( gender= gender)


        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context


class ResearcherRegistrationsListView(FilterView):
    model = ResearcherRegistrations
    template_name = 'dashboard/registrations/v2/researcher_registrations_list.html'
    filterset_class = ResearcherRegistrationsFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'year_of_establishment':
            queryset = queryset.order_by('year_of_establishment')
        else:
            queryset = queryset.order_by('-id')


        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        district = self.request.GET.get('district')
        department= self.request.GET.get('department')
        institution = self.request.GET.get('institution')
        gender = self.request.GET.get('gender')
        state=self.request.GET.get('state')
        highest_qualification = self.request.GET.get('highest_qualification')
        publications = self.request.GET.get('publications')

      
        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if department:
            filters &= Q(department=department)
        if institution:
            filters &= Q(institution=institution)
        if gender:
            filters &= Q(gender=gender)
        if state:
            filters &= Q(state=state)
        if highest_qualification:
            filters &= Q(highest_qualification=highest_qualification)
        if publications:
            filters &= Q(publications=publications)
      

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context



class StudentRegistrationsListView(FilterView):
    model = StudentRegistrations
    template_name = 'dashboard/registrations/v2/student_registrations_list.html'
    filterset_class = StudentRegistrationsFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'area_of_interest':
            queryset = queryset.order_by('area_of_interest')
        else:
            queryset = queryset.order_by('-id')


        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        district = self.request.GET.get('district')
        department= self.request.GET.get('department')
        institution=self.request.GET.get('institution')
        gender=self.request.GET.get('gender')
        state=self.request.GET.get('state')
        highest_qualification=self.request.GET.get('highest_qualification')
        paper_published=self.request.GET.get('paper_published')
      
        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if department:
            filters &= Q(department=department)
        if institution:
            filters &= Q(institution=institution)
        if gender:
            filters &= Q(gender=gender)
        if state:
            filters &= Q(state=state)
        if highest_qualification:
            filters &= Q(highest_qualification=highest_qualification)
        if paper_published:
            filters &= Q(paper_published=paper_published)
      

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context


class VCRegistrationsListView(FilterView):
    model = VCRegistrations
    template_name = 'dashboard/registrations/v2/vc_registrations_list.html'
    filterset_class = VCRegistrationsFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'firm_name':
            queryset = queryset.order_by('firm_name')
        elif sort_by == 'area_of_interest':
            queryset = queryset.order_by('area_of_interest')
        else:
            queryset = queryset.order_by('-id')
  

        # Apply filters
        filters = Q()
        state=self.request.GET.get('state')
        fund_type=self.request.GET.get('fund_type')
        area_of_interest = self.request.GET.get('area_of_interest')
        district = self.request.GET.get('district')
        funding_stage = self.request.GET.get('funding_stage')
      
        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if funding_stage:
            filters &= Q(funding_stage=funding_stage)
        if state:
            filters &= Q(state=state)
        if fund_type:
            filters &= Q(fund_type=fund_type)

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context



class IndustryRegistrationsListView(FilterView):
    model = IndustryRegistrations
    template_name = 'dashboard/registrations/v2/industry_registrations_list.html'
    filterset_class = IndustryRegistrationsFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        # Apply sorting
        sort_by = self.request.GET.get('sort_by')
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'area_of_interest':
            queryset = queryset.order_by('area_of_interest')
        else:
            queryset = queryset.order_by('-id')
  

        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        district = self.request.GET.get('district')
        industry = self.request.GET.get('industry')
        state= self.request.GET.get('state')
      
        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if industry:
            filters &= Q(industry=industry)
        if state:
            filters &= Q(state=state)

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context

