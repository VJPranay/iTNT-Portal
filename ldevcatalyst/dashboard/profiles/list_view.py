from django.views.generic import ListView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.db.models import Q
from profiles.models import StartUp, Industry, Researcher, Student, VC, Industry
from .list_view_filters import StartUpFilter, ResearcherFilter, StudentFilter, VCFilter, IndustryFilter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required



class StartUpListView(FilterView):
    model = StartUp
    template_name = 'dashboard/profiles/v2/startup_list.html'
    filterset_class = StartUpFilter
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
        preferred_investment_stage = self.request.GET.get('preferred_investment_stage')
        state=self.request.GET.get('state')
        fund_raised=self.request.GET.get('fund_raised')
        development_stage=self.request.GET.get('development_stage')
        gender=self.request.GET.get('gender')
        primary_business_model=self.request.GET.get('primary_business_model')
        reveune_stage=self.request.GET.get('reveune_stage')
        dpiit_number=self.request.GET.get('dpiit_number')

        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if year_of_establishment:
            filters &= Q(year_of_establishment=year_of_establishment)
        if district:
            filters &= Q(district=district)
        if preferred_investment_stage:
            filters &= Q(preferred_investment_stage=preferred_investment_stage)
        if  state:
            filters &= Q(state=state)
        if fund_raised:
            filters &= Q(fund_raised=fund_raised)
        if development_stage:
            filters &= Q(development_stage=development_stage)
        if gender:
            filters &= Q(gender=gender)
        if  primary_business_model:
            filters &= Q( primary_business_model= primary_business_model)
        if  reveune_stage:
            filters &= Q( reveune_stage= reveune_stage)
        if   dpiit_number:
            filters &= Q(  dpiit_number=  dpiit_number)


        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context



class ResearcherListView(FilterView):
    model = Researcher
    template_name = 'dashboard/profiles/v2/researcher_list.html'
    filterset_class = ResearcherFilter
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




class StudentListView(FilterView):
    model = Student
    template_name = 'dashboard/profiles/v2/student_list.html'
    filterset_class = StudentFilter
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
        year_of_graduation=self.request.GET.get('year_of_graduation')
      
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
        if year_of_graduation:
            filters &= Q(year_of_graduation=year_of_graduation)
      

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context


class VCListView(FilterView):
    model = VC
    template_name = 'dashboard/profiles/v2/vc_list.html'
    filterset_class = VCFilter
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
        funding_stage = self.request.GET.get('funding_stage')
      
        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if funding_stage:
            filters &= Q(funding_stage=funding_stage)

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context




class IndustryListView(FilterView):
    model = Industry
    template_name = 'dashboard/profiles/v2/industry_list.html'
    filterset_class = IndustryFilter
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
      
        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if industry:
            filters &= Q(industry=industry)

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context


