from django.views.generic import ListView
from django_filters.views import FilterView
from django.core.paginator import Paginator
from django.db.models import Q
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from smeconnect.models import MeetingRequest
from .list_view_filters import SmeConnectFilter



class SmeConnectListView(FilterView):
    model = MeetingRequest
    template_name = 'dashboard/meetings/v2/sme_connect_list.html'
    filterset_class = SmeConnectFilter
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()

        filters = Q()

        sender=self.request.GET.get('sender')
        receiver=self.request.GET.get('receiver')
        meeting_type=self.request.GET.get('meeting_type')
        status=self.request.GET.get('status')

        if sender:
            filters &= Q(sender=sender)
        if receiver:
            filters &= Q(receiver=receiver)
        if meeting_type:
            filters &= Q(meeting_type=meeting_type)
        if status:
            filters &= Q(status=status)
       
        queryset = queryset.filter(filters)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'].form.helper = FormHelper()
        context['filter'].form.helper.form_method = 'get'
        context['filter'].form.helper.add_input(Submit('submit', 'Apply Filters', css_class='btn btn-primary'))
        context['filter_params'] = self.request.GET.urlencode()  # Adding filter params to context
        return context

