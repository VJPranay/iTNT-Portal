from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from smeconnect.models import MeetingRequest
from mentorstartupconnect.models import MentorStartupMeetingRequest
from smeindustryconnect.models import SmeIndustryMeetingRequest
from vcstartup_meetings.models import vcstartup_MeetingRequest


@login_required
def sme_connect_details(request, pk):
    try:
        meeting = MeetingRequest.objects.get(pk=pk)
        return render(request, 'dashboard/meetings/v2/sme_connect_details.html', {'meeting': meeting})
    except MeetingRequest.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    
    
@login_required
def vcstartup_connect_details(request, pk):
    try:
        meeting = vcstartup_MeetingRequest.objects.get(pk=pk)
        return render(request, 'dashboard/meetings/v2/vcstartup_connect_details.html', {'meeting': meeting})
    except MeetingRequest.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    
@login_required
def smeindustry_connect_details(request, pk):
    try:
        meeting = SmeIndustryMeetingRequest.objects.get(pk=pk)
        return render(request, 'dashboard/meetings/v2/smeindustry_connect_details.html', {'meeting': meeting})
    except MeetingRequest.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    

@login_required
def mentorstartup_connect_details(request, pk):
    try:
        meeting = MentorStartupMeetingRequest.objects.get(pk=pk)
        return render(request, 'dashboard/meetings/v2/mentorstartup_connect_details.html', {'meeting': meeting})
    except MeetingRequest.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))