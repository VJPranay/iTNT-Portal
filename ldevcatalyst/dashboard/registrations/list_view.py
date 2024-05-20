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
        else:
            queryset = queryset.order_by('-id')

        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        state = self.request.GET.get('state')
        dpiit_number = self.request.GET.get('dpiit_number')
        reveune_stage = self.request.GET.get('reveune_stage')
        # gender = self.request.GET.get('gender')
        development_stage = self.request.GET.get('development_stage')
        primary_business_model = self.request.GET.get('primary_business_model')
        district = self.request.GET.get('district')
        preferred_investment_stage = self.request.GET.get('preferred_investment_stage')

        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if primary_business_model:
            filters &= Q(primary_business_model=primary_business_model)
        if dpiit_number:
            filters &= Q(dpiit_number=dpiit_number)
        if state:
            filters &= Q(state=state)
        if reveune_stage:
            filters &= Q(reveune_stage=reveune_stage)
        # if gender:
            # filters &= Q(gender=gender)
        if development_stage:
            filters &= Q(development_stage=development_stage)
        if district:
            filters &= Q(district=district)
        if preferred_investment_stage:
            filters &= Q(preferred_investment_stage=preferred_investment_stage)

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
        state= self.request.GET.get('state')
        institution= self.request.GET.get('institution')
        gender= self.request.GET.get('gender')
        highest_qualification= self.request.GET.get('highest_qualification')
        publications= self.request.GET.get('publications')

        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if department:
            filters &= Q(department=department)
        if state:
            filters &= Q(state=state)
        if institution:
            filters &= Q(institution=institution)
        if gender:
            filters &= Q(gender=gender)
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
      
        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if department:
            filters &= Q(department=department)
      

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
        area_of_interest = self.request.GET.get('area_of_interest')
        district = self.request.GET.get('district')

        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)

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
        elif sort_by == 'industry':
            queryset = queryset.order_by('industry')
        else:
            queryset = queryset.order_by('-id')

        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        industry = self.request.GET.get('industry')
        district = self.request.GET.get('district')


        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if industry:
            filters &= Q(industry=industry)
        if district:
            filters &= Q(district=district)

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context

