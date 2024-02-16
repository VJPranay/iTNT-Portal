from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
import random
from profiles.models import StartUp
from .models import MeetingRequests
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


# Create your views here.
@login_required
def vc_meeting_requests(request):
    if request.user.user_role ==  8:
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

@login_required
def fetch_startup_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        area_of_interest_id = data.get('area_of_interest_id')
        if not area_of_interest_id:
            return JsonResponse([], safe=False)
        vc_meetings_reqests_startup_ids = MeetingRequests.objects.filter(vc_id=request.user.id, status='pending', start_up__area_of_interest=area_of_interest_id).values_list('start_up', flat=True)
        startup_profiles = StartUp.objects.filter(id__in=vc_meetings_reqests_startup_ids)
        # Prepare data to be sent as JSON response
        profiles_data = []
        for profile in startup_profiles:
            profiles_data.append({
                'startup_id': profile.id,
                'startup_name': profile.name,
                'funding_stage': profile.funding_stage.name,
            })
        return JsonResponse(profiles_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    
@login_required
def fetch_startup_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        startup_id = data.get('startup_id',None)
        if not startup_id:
            return JsonResponse({'error': 'Invalid startup ID'}, status=400)
        # Fetch startup details based on startup_id
        print(startup_id)
        startup = StartUp.objects.get(id=startup_id)
        # Construct HTML for the startup details
        html = f"""
            <!-- HTML for startup details -->
            <div class="d-flex gap-7 align-items-center">
                <!-- Avatar -->
                <div class="symbol symbol-circle symbol-100px">
                    <span class="symbol-label bg-light-success fs-1 fw-bolder">{startup.name[:1]}</span>
                </div>
                <!-- Contact details -->
                <div class="d-flex flex-column gap-2">
                    <h3 class="mb-0">{startup.name}</h3>
                    <div class="d-flex align-items-center gap-2">
                        <i class="ki-outline ki-sms fs-2"></i>
                        <span class="text-muted text-hover-primary">{startup.area_of_interest.name}</span>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                        <i class="ki-outline ki-phone fs-2"></i>
                        <span class="text-muted text-hover-primary">{startup.funding_stage.name}</span>
                    </div>
                    <!-- Add other details as needed -->
                </div>
            </div>
            <!-- Additional details -->
            <div class="d-flex flex-column gap-5 mt-7">
                <!-- Add other details as needed -->
            </div>
        """
        # Send the HTML response to the JavaScript function
        return JsonResponse({'html': html})
    else:
        # Handle invalid request
        return JsonResponse({'error': 'Invalid request'}, status=400)