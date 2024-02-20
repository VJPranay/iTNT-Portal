from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datarepo.models import AreaOfInterest

from profiles.models import Researcher
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

from ..models import Researcher
# Create your views here.


@login_required
def sme_list(request):
    # Get all areas of interests with profile count
    areas_q = AreaOfInterest.objects.all()
    areas_list = []
    for x in areas_q:
        temp = {
            'id': x.id,
            'name': x.name,
            'count': Researcher.objects.filter(
                area_of_interest=x  # Adjusted to match the many-to-many relationship
            ).count()
        }
        areas_list.append(temp)
    template_data = {
        'areas_list': areas_list
    }
    return render(request, 'dashboard/profiles/sme/list.html', context=template_data)



@require_POST
@login_required
def fetch_sme_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        area_of_interest_ids = data.get('area_of_interest', None)
        if not area_of_interest_ids:
            return JsonResponse({'error': 'Area of Interest ID(s) are required'}, status=400)
        sme_profiles_q = Researcher.objects.filter(
            area_of_interest__id=area_of_interest_ids
        ) # Ensure unique sme profiles
        
        sme_profiles = []
        for profile in sme_profiles_q:
            sme_profiles.append({
                'sme_id': profile.id,
                'name': profile.name,
                'department': profile.department.name,
            })
        return JsonResponse(sme_profiles, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
def fetch_sme_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        sme_id = data.get('sme_id',None)
        if not sme_id:
            return JsonResponse({'error': 'Invalid sme ID'}, status=400)
        # Fetch startup details based on startup_id
        print(sme_id)
        sme = Researcher.objects.get(id=sme_id)
        # Construct HTML for the startup details
        html = f"""
                                    <!--begin::Profile-->
                                    <div class="d-flex gap-7 align-items-center">
                                        <!--begin::Avatar-->
                                        <div class="symbol symbol-circle symbol-200px">
                                            <span class="symbol-label bg-light-success fs-1 fw-bolder">{sme.user}</span>
                                        </div>
                                        <!--end::Avatar-->
                                        <!--begin::Contact details-->
                                        <div class="d-flex flex-column gap-2">
                                            <!--begin::Name-->
                                            <h3 class="mb-0">{sme.name}</h3>
                                            <!--end::Name-->
                                            <!--begin::Email-->
                                            <div class="d-flex align-items-center gap-2">
                                                <i class="ki-outline ki-sms fs-2"></i>
                                                <a href="#" class="text-muted text-hover-primary">{sme.area_of_interest}</a>
                                            </div>
                                            <!--end::Email-->
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
                                                    <div class="fw-bold fs-5">{sme.state.name}</div>
                                                </div>
                                                <!--end::state-->
                                                <!--begin::district-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">District</div>
                                                    <div class="fw-bold fs-5">{sme.district.name}</div>
                                                </div>
                                                <!--end::district-->
                                                <!--begin::department-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Department</div>
                                                    <div class="fw-bold fs-5">{sme.department}</div>
                                                </div>
                                                <!--end::department-->
                                                <!--begin::institution-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Institution</div>
                                                    <div class="fw-bold fs-5">{sme.institution}</div>
                                                </div>
                                                <!--end::institution-->
                                                <!--begin::mobile-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Mobile</div>
                                                    <div class="fw-bold fs-5">{sme.mobile}</div>
                                                </div>
                                                <!--end::mobile-->
                                                <!--end::picture-->
                                                <!--begin::highest_qualification-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Highest Qualification</div>
                                                    <div class="fw-bold fs-5">{sme.highest_qualification}</div>
                                                </div>
                                              <!--end::publications-->
                                              <!-- begin::number -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Patent Number</div>
                                                    <div class="fw-bold fs-5">{sme.patents.number}</div>
                                                </div>
                                                <!-- end::number-->

                                                <!-- begin::title -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Title</div>
                                                    <div class="fw-bold fs-5">{sme.patents.title}</div>
                                                </div>
                                                <!-- end::title -->

                                                <!-- begin::inventors -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Inventors</div>
                                                    <div class="fw-bold fs-5">{sme.patents.inventors}</div>
                                                </div>
                                                <!-- end::inventors -->

                                                <!-- begin::filing_date -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Filing Date</div>
                                                    <div class="fw-bold fs-5">{sme.patents.filing_date}</div>
                                                </div>
                                                <!-- end::filing_date -->

                                                <!-- begin::status -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Status</div>
                                                    <div class="fw-bold fs-5">{sme.patents.status}</div>
                                                </div>
                                                <!-- end::status -->

                                                <!-- begin::paper_title -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Paper Title</div>
                                                    <div class="fw-bold fs-5">{sme.publications.title}</div>
                                                </div>
                                                <!-- end::paper_title -->

                                                <!-- begin::paper_link -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Paper Link</div>
                                                    <div class="fw-bold fs-5">{sme.publications.paper_link}</div>
                                                </div>
                                                <!-- end::paper_link -->

                                                <!-- begin::journal -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Journal</div>
                                                    <div class="fw-bold fs-5">{sme.publications.journal}</div>
                                                </div>
                                                <!-- end::journal -->

                                                

                                                
                                               
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
    