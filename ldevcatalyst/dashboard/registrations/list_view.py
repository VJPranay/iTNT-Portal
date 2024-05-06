from django.views.generic import ListView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.db.models import Q
from registrations.models import StartUpRegistrations
from .list_view_filters import StartUpRegistraionsFilter
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required



class StartUpRegistrtaionsListView(FilterView):
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

        # Apply filters
        filters = Q()
        area_of_interest = self.request.GET.get('area_of_interest')
        district = self.request.GET.get('district')
        preferred_investment_stage = self.request.GET.get('preferred_investment_stage')

        if area_of_interest:
            filters &= Q(area_of_interest=area_of_interest)
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

@login_required
def startup_profile_details(request, pk):
    try:
        startup = StartUpRegistrations.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/startup_profile_details.html', {'startup': startup})
    except StartUpRegistrations.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    

