from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datarepo.models import AreaOfInterest
from profiles.models import VC
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
from profiles.models import StartUp
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from .models import VC
# Create your views here.


@login_required
def vc_list(request):
    #get all area of interests with profile count
    areas_q = AreaOfInterest.objects.all()
    areas_list = []
    for x in areas_q:
        temp = {
            'id' : x.id,
            'name' : x.name,
            'count' : VC.objects.filter(
                area_of_interest_id = x.id
            ).count()
        }
        areas_list.append(temp)
    template_data = {
        'areas_list' : areas_list
    }
    return render(request,'dashboard/profiles/vc/list.html',context=template_data)


@login_required
def fetch_vc_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        area_of_interest_id = data.get('area_category_id')
        if not area_of_interest_id:
            return JsonResponse([], safe=False)
        vc_profiles_q = VC.objects.filter(
            area_of_interest_id = area_of_interest_id
        )
        vc_profiles = []
        for profile in vc_profiles_q:
            vc_profiles.append({
                'vc_id': profile.id,
                'firm_name': profile.firm_name,
                'funding_stage': profile.funding_stage.name,
            })
        return JsonResponse(vc_profiles, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    
@login_required
def fetch_vc_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        vc_id = data.get('vc_id',None)
        if not vc_id:
            return JsonResponse({'error': 'Invalid vc ID'}, status=400)
        # Fetch startup details based on startup_id
        print(vc_id)
        vc = VC.objects.get(id=vc_id)
        # Construct HTML for the startup details
        html = f"""
            <!-- HTML for vc details -->
            <div class="d-flex gap-7 align-items-center">
                <!-- Avatar -->
                <div class="symbol symbol-circle symbol-100px">
                    <span class="symbol-label bg-light-success fs-1 fw-bolder">{vc.partner_name[:1]}</span>
                </div>
                <!-- Contact details -->
                <div class="d-flex flex-column gap-2">
                    <h3 class="mb-0">{vc.partner_name}</h3>
                    <div class="d-flex align-items-center gap-2">
                        <i class="ki-outline ki-sms fs-2"></i>
                        <span class="text-muted text-hover-primary">{vc.area_of_interest.name}</span>
                    </div>
                    <div class="d-flex align-items-center gap-2">
                        <i class="ki-outline ki-phone fs-2"></i>
                        <span class="text-muted text-hover-primary">{vc.funding_stage.name}</span>
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
    