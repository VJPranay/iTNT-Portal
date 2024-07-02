from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from smeconnect.models import MeetingRequest


@login_required
def sme_connect_details(request, pk):
    try:
        meeting = MeetingRequest.objects.get(pk=pk)
        return render(request, 'dashboard/meetings/v2/sme_connect_details.html', {'meeting': meeting})
    except MeetingRequest.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    
    
