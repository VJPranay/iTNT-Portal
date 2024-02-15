from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
import random
from profiles.models import StartUp
from .models import MeetingRequests
from django.db.models import Count


# Create your views here.
@login_required
def vc_meeting_requests(request):
    if request.user.user_role ==  8:
        # load the categories
        # load profiles from frist category loaded
        # load profile details from the first profile
        template_data = {
            'interest_areas_data' : MeetingRequests.objects.filter(vc_id=request.user.id,status='pending').values('start_up__area_of_interest__id', 'start_up__area_of_interest__name').annotate(requests_count=Count('id')),
            'start_up_profiles' : []
        }
        print(template_data)
        return render(request,'dashboard/meetings/vc/meeting_requests.html',context=template_data)
    else:
        return HttpResponseRedirect(reverse('not_found'))