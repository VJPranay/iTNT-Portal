from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datarepo.models import AreaOfInterest

from profiles.models import StartUp
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
from profiles.models import StartUp
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.utils.html import escape
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from meetings.models import MeetingRequests


# Create your views here.


@login_required
def startup_list(request):
    # Get all areas of interests with profile count
    areas_q = AreaOfInterest.objects.filter(is_approved=True)
    areas_list = []
    for x in areas_q:
        temp = {
            'id': x.id,
            'name': x.name,
            'count': StartUp.objects.filter(
                area_of_interest=x  # Adjusted to match the many-to-many relationship
            ).count()
        }
        areas_list.append(temp)
    template_data = {
        'areas_list': areas_list
    }
    return render(request, 'dashboard/profiles/startup/list.html', context=template_data)



@login_required
def fetch_startup_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        area_of_interest_ids = data.get('area_of_interest', None)
        if not area_of_interest_ids:
            return JsonResponse({'error': 'Area of Interest ID(s) are required'}, status=400)
        startup_profiles_q = StartUp.objects.filter(
            area_of_interest__id=area_of_interest_ids
        ) # Ensure unique startup profiles

        startup_profiles = []
        for profile in startup_profiles_q:
            startup_profiles.append({
                'startup_id': profile.id,
                'name': profile.name,
                'email': profile.email,
            })
        return JsonResponse(startup_profiles, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
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
                                                        <div class="d-flex gap-7 align-items-center" id="startupid" data-startup-id=""""+escape(startup.id)+"""">
                                                        <!--begin::Profile-->
                                                        <div class="d-flex gap-7 align-items-center">
                                                            <!--begin::Avatar-->
                                                            <div class="symbol symbol-circle symbol-100px">
                                                                <span class="symbol-label bg-light-success fs-1 fw-bolder">"""+escape(startup.name[:1])+"""</span>
                                                            </div>
                                                            <!--end::Avatar-->
                                                            <!--begin::Contact details-->
                                                            <div class="d-flex flex-column gap-2">
                                                                <!--begin::Name-->
                                                                <h3 class="mb-0">"""+escape(startup.name)+"""</h3>
                                                                <!--end::Name-->
                                                                <!--begin::Email-->
                                                                <div class="d-flex align-items-center gap-2">
                                                                    <i class="ki-outline ki-sms fs-2"></i>
                                                                    <a href="#" class="text-muted text-hover-primary">"""+escape(startup.area_of_interest)+"""</a>
                                                                </div>
                                                                <!--end::Email-->
                                                                <!--begin::Phone-->
                                                                <div class="d-flex align-items-center gap-2">
                                                                    <i class="ki-outline ki-phone fs-2"></i>
                                                                    <a href="#" class="text-muted text-hover-primary">"""+escape(startup.funding_stage.name)+"""</a>
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
                                                                    <!--begin::Company description-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Pitch Deck</div>
                                                                        <iframe width="560" height="315" src="https://docs.google.com/presentation/d/"""+escape(startup.pitch_deck)+"""/embed?start=false&loop=false" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
                                                                    </div>
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Short video</div>
                                                                        <iframe width="560" height="315" src="https://www.youtube.com/embed/"""+escape(startup.short_video)+""" frameborder="0" allowfullscreen></iframe>
                                                                    </div>
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Description</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.description)+"""</div>
                                                                    </div>
                                                                    <!--end::Company description-->
                                                                    <!--begin::market_size-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Market size</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.market_size)+"""</div>
                                                                    </div>
                                                                    <!--end::market_size-->
                                                                    <!--begin::funding_stage-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Current funding stage</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.funding_stage.name)+"""</div>
                                                                    </div>
                                                                    <!--end::funding_stage-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Industry</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.area_of_interest.name)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Requried Amount</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.required_amount)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Founding year</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.founding_year)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Co-Founder team size </div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.co_founder_team_size)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Total team size</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.total_team_size)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Founding experince</div>
                                                                        <div class="fw-bold fs-5">"""+escape( "yes" if startup.founding_experience else "no")+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">State</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.state.name)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::district-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">City</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.city)+"""</div>
                                                                    </div>
                                                                    <!--end::district-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Full Video</div>
                                                                        <iframe width="560" height="315" src="https://www.youtube.com/embed/"""+escape(startup.full_video)+""" frameborder="0" allowfullscreen></iframe>
                                                                    </div>
                    
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
    