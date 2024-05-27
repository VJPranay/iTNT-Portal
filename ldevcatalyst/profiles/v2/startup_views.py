from django.views.generic import ListView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.db.models import Q
from profiles.models import StartUp
from .startup_filters import StartUpFilter
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
        if sort_by == 'name':
            queryset = queryset.order_by('name')
        elif sort_by == 'founding_year':
            queryset = queryset.order_by('founding_year')

        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        district = self.request.GET.get('district')
        founding_experience = self.request.GET.get('founding_experience')

        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
        if district:
            filters &= Q(district=district)
        if founding_experience:
            filters &= Q(founding_experience=True)

        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        return context


    

