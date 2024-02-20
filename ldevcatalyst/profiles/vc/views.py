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
from ..models import VC
from django.utils.html import escape
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
            	<!--begin::Profile-->
													<div class="d-flex gap-7 align-items-center" id="vcid" data-vc-id=""""+escape(vc.id)+"""">
														<!--begin::Avatar-->
														<div class="symbol symbol-circle symbol-100px">
															<span class="symbol-label bg-light-success fs-1 fw-bolder">"""+escape(vc.firm_name[:1])+"""</span>
														</div>
														<!--end::Avatar-->
														<!--begin::Contact details-->
														<div class="d-flex flex-column gap-2">
															<!--begin::Name-->
															<h3 class="mb-0">"""+escape(vc.firm_name)+"""</h3>
															<!--end::Name-->
															<!--begin::Email-->
															<div class="d-flex align-items-center gap-2">
																<i class="ki-outline ki-sms fs-2"></i>
																<a href="#" class="text-muted text-hover-primary">"""+escape(vc.area_of_interest.name)+"""</a>
															</div>
															<!--end::Email-->
															<!--begin::Phone-->
															<div class="d-flex align-items-center gap-2">
																<i class="ki-outline ki-phone fs-2"></i>
																<a href="#" class="text-muted text-hover-primary">"""+escape(vc.funding_stage.name)+"""</a>
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

																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Partner Name</div>
																	<div class="fw-bold fs-5">"""+escape(vc.partner_name)+"""</div>
																</div>
																<!--end::Company description-->
																<!--begin::market_size-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Market size</div>
																	<div class="fw-bold fs-5">"""+escape(vc.deal_size_range)+"""</div>
																</div>
																<!--end::market_size-->
																<!--begin::funding_stage-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Portfolio size</div>
																	<div class="fw-bold fs-5">"""+escape(vc.portfolio_size)+"""</div>
																</div>
																<!--end::funding_stage-->
                											    <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">District</div>
																	<div class="fw-bold fs-5">"""+escape(vc.district)+"""</div>
																</div>
																<!--end::area_of_interest-->
                                								<!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">State</div>
																	<div class="fw-bold fs-5">"""+escape(vc.state)+"""</div>
																</div>
																<!--end::area_of_interest-->
                                                			    <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">LinkedIn</div>
																	<a href="{vc.linkedin_profile}"><div class="fw-bold fs-5">"""+escape(vc.linkedin_profile)+"""</div></a>
																</div>
																<!--end::area_of_interest-->
                                                                <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Website</div>
																	<a href="{vc.linkedin_profile}"><div class="fw-bold fs-5">"""+escape(vc.company_website)+"""</div></a>
																</div>
                
															</div>
															<!--end::Additional details-->
														</div>
														<!--end:::Tab pane-->
													</div>
													<!--end::Tab content-->  """
        # Send the HTML response to the JavaScript function
        return JsonResponse({'html': html})
    else:
        # Handle invalid request
        return JsonResponse({'error': 'Invalid request'}, status=400)
    