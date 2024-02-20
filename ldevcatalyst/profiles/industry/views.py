from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datarepo.models import AreaOfInterest

from profiles.models import Industry
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
from profiles.models import StartUp
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json


# Create your views here.


@login_required
def industry_list(request):
    # Get all areas of interests with profile count
    areas_q = AreaOfInterest.objects.all()
    areas_list = []
    for x in areas_q:
        temp = {
            'id': x.id,
            'name': x.name,
            'count': Industry.objects.filter(
                area_of_interest=x  # Adjusted to match the many-to-many relationship
            ).count()
        }
        areas_list.append(temp)
    template_data = {
        'areas_list': areas_list
    }
    return render(request, 'dashboard/profiles/industry/list.html', context=template_data)



@require_POST
@login_required
def fetch_industry_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        area_of_interest_ids = data.get('area_of_interest', None)
        if not area_of_interest_ids:
            return JsonResponse({'error': 'Area of Interest ID(s) are required'}, status=400)
        industry_profiles_q = Industry.objects.filter(
            area_of_interest__id=area_of_interest_ids
        ) # Ensure unique industry profiles
        
        industry_profiles = []
        for profile in industry_profiles_q:
            industry_profiles.append({
                'industry_id': profile.id,
                'name': profile.name,
                'industry':profile.industry.name
            })
        return JsonResponse(industry_profiles, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
def fetch_industry_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        industry_id = data.get('industry_id',None)
        if not industry_id:
            return JsonResponse({'error': 'Invalid industry ID'}, status=400)
        # Fetch startup details based on startup_id
        print(industry_id)
        industry = Industry.objects.get(id=industry_id)
        # Construct HTML for the startup details
        html = f"""
                                            <!--begin::Profile-->
                                            <div class="d-flex gap-7 align-items-center">
                                                <!--begin::Avatar-->
                                                <div class="symbol symbol-circle symbol-200px">
                                                    <span class="symbol-label bg-light-success fs-1 fw-bolder">{industry.user}</span>
                                                </div>
                                                <!--end::Avatar-->
                                                <!--begin::Contact details-->
                                                <div class="d-flex flex-column gap-2">
                                                    <!--begin::Name-->
                                                    <h3 class="mb-0">{industry.name}</h3>
                                                    <!--end::Name-->
                                                    <!--begin::Email-->
                                                    <div class="d-flex align-items-center gap-2">
                                                        <i class="ki-outline ki-sms fs-2"></i>
                                                        <a href="#" class="text-muted text-hover-primary">{industry.mobile}</a>
                                                    </div>
                                                    <!--end::Email-->
                                                    <!--begin::Phone-->
                                                    <div class="d-flex align-items-center gap-2">
                                                        <i class="ki-outline ki-phone fs-2"></i>
                                                        <a href="#" class="text-muted text-hover-primary">{industry.email}</a>
                                                    </div>
                                                    <!--end::Phone-->
                                                </div>
                                                <!--end::Contact details-->
                                            </div>
                                            <!--end::Profile-->
                                            <!--begin:::Tabs-->
                                            <ul class="nav nav-custom nav-tabs nav-line-tabs nav-line-tabs-2x fs-6 fw-semibold mt-6 mb-8 gap-2">
                                                <!--begin:::Tab item-->
                                                <li class="nav-item">
                                                    <a class="nav-link text-active-primary d-flex align-items-center pb-4 active" data-bs-toggle="tab" href="#kt_contact_view_general">
                                                    <i class="ki-outline ki-home fs-4 me-1"></i>Information</a>
                                                </li>
                                                <!--end:::Tab item-->
                                            </ul>
                                            <!--end:::Tabs-->
                                            <!--begin::Tab content-->
                                            <div class="tab-content" id="">
                                                <!--begin:::Tab pane-->
                                                <div class="tab-pane fade show active" id="kt_contact_view_general" role="tabpanel">
                                                    <!--begin::Additional details-->
                                                    <div class="d-flex flex-column gap-5 mt-7">
                                                        <!--begin::state-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">State</div>
                                                            <div class="fw-bold fs-5">{industry.state}</div>
                                                        </div>
                                                        <!--end::state-->
                                                        <!--begin::district-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">District</div>
                                                            <div class="fw-bold fs-5">{industry.district}</div>
                                                        </div>
                                                        <!--end::district-->
                                                       
                                                        <!--end::end year_of_graduation-->
                                                        <!--begin::point_of_contact_name-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">point of contact name</div>
                                                            <div class="fw-bold fs-5">{industry.point_of_contact_name}</div>
                                                        </div>
                                                        <!--end::point_of_contact_name-->
                                                
                                                        
                                                        <!--begin::mobile-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">Industry</div>
                                                            <div class="fw-bold fs-5">{industry.industry}</div>
                                                        </div>
                                                        <!--end::mobile-->
                                                        <!--begin::area_of_interest-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">Area of Interest</div>
                                                            <div class="fw-bold fs-5">{industry.area_of_interest}</div>
                                                        </div>
                                                        <!--end::area_of_interest-->
                                                        
                                                    </div>
                                                    <!--end::Additional details-->
                                                </div>
                                                <!--end:::Tab pane-->
                                            </div>
                                            <!--end::Tab content-->
            """

        # Send the HTML response to the JavaScript function
        return JsonResponse({'html': html})
    else:
        # Handle invalid request
        return JsonResponse({'error': 'Invalid request'}, status=400)
    