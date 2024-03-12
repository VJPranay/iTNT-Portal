from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
import random
from profiles.models import StartUp
from .models import MeetingRequests
from django.db.models import Count
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from profiles.models import VC ,Student,Industry
from .models import MeetingRequests
from django.utils.html import escape
from .forms import MeetingRequestUpdateForm
from django.http import JsonResponse


# Create your views here.
@login_required
def vc_meeting_requests(request):
    if request.user.user_role ==  8:
        # load profiles from frist category loaded
        # load profile details from the first profile
        vc_profile_id = VC.objects.get(user_id=request.user.id).id
        template_data = {
            'interest_areas_data' : MeetingRequests.objects.filter(vc_id=vc_profile_id,status='pending').values('start_up__area_of_interest__id', 'start_up__area_of_interest__name').annotate(requests_count=Count('id')),
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
        vc_profile_id = VC.objects.get(user_id=request.user.id).id
        vc_meetings_reqests_startup_ids = MeetingRequests.objects.filter(vc_id=vc_profile_id, status='pending', start_up__area_of_interest=area_of_interest_id).values_list('start_up', flat=True)
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
        startup = StartUp.objects.get(id=startup_id)
        # Construct HTML for the startup details
        html = f"""
           													<!--begin::Profile-->
													<div class="d-flex gap-7 align-items-center" id="startup-id" data-startup-id="{startup.id}">
														<!--begin::Avatar-->
														<div class="symbol symbol-circle symbol-100px">
															<span class="symbol-label bg-light-success fs-1 fw-bolder">{startup.name[:1]}</span>
														</div>
														<!--end::Avatar-->
														<!--begin::Contact details-->
														<div class="d-flex flex-column gap-2">
															<!--begin::Name-->
															<h3 class="mb-0">{startup.name}</h3>
															<!--end::Name-->
															<!--begin::Email-->
															<div class="d-flex align-items-center gap-2">
																<i class="ki-outline ki-sms fs-2"></i>
																<a href="#" class="text-muted text-hover-primary">{startup.area_of_interest.name}</a>
															</div>
															<!--end::Email-->
															<!--begin::Phone-->
															<div class="d-flex align-items-center gap-2">
																<i class="ki-outline ki-phone fs-2"></i>
																<a href="#" class="text-muted text-hover-primary">{startup.funding_stage.name}</a>
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
                                                                    <iframe width="560" height="315" src="https://docs.google.com/presentation/d/{startup.pitch_deck}/embed?start=false&loop=false" frameborder="0" allowfullscreen="true" mozallowfullscreen="true" webkitallowfullscreen="true"></iframe>
                                                                </div>
                                                                 <div class="d-flex flex-column gap-1">
                                                                    <div class="fw-bold text-muted">Short video</div>
                                                                    <iframe width="560" height="315" src="https://www.youtube.com/embed/{startup.short_video}" frameborder="0" allowfullscreen></iframe>
                                                                </div>
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Description</div>
																	<div class="fw-bold fs-5">{startup.description}</div>
																</div>
																<!--end::Company description-->
                                                                 <!--begin::dpiit number-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">DPIIT number</div>
																	<div class="fw-bold fs-5">{startup.dpiit_number}</div>
																</div>
																<!--end::dpiit number-->
                                                                <!--begin::Website-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Website</div>
																	<div class="fw-bold fs-5">{startup.website}</div>
																</div>
																<!--end::=Website-->
                                                                 <!--begin::Website-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Email</div>
																	<div class="fw-bold fs-5">{startup.email}</div>
																</div>
																<!--end::=Website-->
																<!--begin::market_size-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Market size</div>
																	<div class="fw-bold fs-5">{startup.market_size}</div>
																</div>
																<!--end::market_size-->
																<!--begin::funding_stage-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Current funding stage</div>
																	<div class="fw-bold fs-5">{startup.funding_stage.name}</div>
																</div>
																<!--end::funding_stage-->
                											    <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Industry</div>
																	<div class="fw-bold fs-5">{startup.area_of_interest.name}</div>
																</div>
																<!--end::area_of_interest-->
                                								<!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Requried Amount</div>
																	<div class="fw-bold fs-5">{startup.required_amount}</div>
																</div>
																<!--end::area_of_interest-->
                                                			    <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Founding year</div>
																	<div class="fw-bold fs-5">{startup.founding_year}</div>
																</div>
																<!--end::area_of_interest-->
                                                                <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Co-Founder team size </div>
																	<div class="fw-bold fs-5">{startup.co_founder_count}</div>
																</div>
																<!--end::area_of_interest-->
                                                                <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Total team size</div>
																	<div class="fw-bold fs-5">{startup.team_size}</div>
																</div>
																<!--end::area_of_interest-->
                                                                <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">Founding experince</div>
																	<div class="fw-bold fs-5">{ "Yes" if startup.founding_experience else "No" }</div>
																</div>
																<!--end::area_of_interest-->
                                                                <!--begin::area_of_interest-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">State</div>
																	<div class="fw-bold fs-5">{startup.state.name}</div>
																</div>
																<!--end::area_of_interest-->
                                                                <!--begin::district-->
																<div class="d-flex flex-column gap-1">
																	<div class="fw-bold text-muted">City</div>
																	<div class="fw-bold fs-5">{startup.district.name}</div>
																</div>
																<!--end::district-->
                                                                 <div class="d-flex flex-column gap-1">
                                                                    <div class="fw-bold text-muted">Full Video</div>
                                                                    <iframe width="560" height="315" src="https://www.youtube.com/embed/{startup.video_link}" frameborder="0" allowfullscreen></iframe>
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
    
@login_required
def vc_meeting_request(request):
    if request.user.user_role == 6:
        vc_id = request.POST.get('vc_id', None)
        if vc_id is None:
            return JsonResponse({'success': 'false'})
        else:
            try:
                vc_info = VC.objects.get(id=vc_id)
                startup_id = StartUp.objects.get(user_id=request.user.id).id
                try:
                    check_meeting = MeetingRequests.objects.get(start_up_id=startup_id, vc_id=vc_info.id, status='pending')
                    return JsonResponse({'success': 'false'})
                except MeetingRequests.DoesNotExist:
                    new_meeting_request = MeetingRequests.objects.create(
                        start_up_id=startup_id,
                        vc_id=vc_info.id,
                        status='pending'
                    )
                    new_meeting_request.save()
                    return JsonResponse({'success': 'true'})
            except VC.DoesNotExist:
                return JsonResponse({'success': 'false'})
    elif request.user.user_role == 8:
        startup_id = request.POST.get('startup_id', None)
        meeting_status = request.POST.get('meeting_status', True)
        meeting_status = True if meeting_status == 'true' else False
        if startup_id is None:
            return JsonResponse({'success': 'false'})
        else:
            try:
                vc_id = VC.objects.get(user_id=request.user.id).id
                check_meeting = MeetingRequests.objects.get(start_up_id=startup_id,vc_id=vc_id, status='pending')
                check_meeting.status = 'accepted' if meeting_status else 'rejected'
                check_meeting.save()
                return JsonResponse({'success': 'true'})
            except MeetingRequests.DoesNotExist:
                return JsonResponse({'success': 'false'})
    else:
        return JsonResponse({'success': 'false'})
    
    

@login_required
def meetings(request,meeting_status=None):
    if meeting_status is not None:
        meeting_requests = MeetingRequests.objects.filter(status=meeting_status)
    else:
        meeting_requests = MeetingRequests.objects.all()
    meeting_requests_list = []
    for x in meeting_requests:
        temp = {
            'meeting_id' : x.id,
            'start_up':x.start_up.name,
            'vc' : x.vc.firm_name,
            'created' : x.created,
            'updated':x.updated,
        }
        meeting_requests_list.append(temp)
    return render(request, 'dashboard/meetings/list.html',context={'meeting_requests':meeting_requests_list})


@login_required
def meeting(request,meeting_id=None):
    if meeting_id is not None:
        meeting_request = MeetingRequests.objects.get(id=meeting_id)
        return render(request, 'dashboard/meetings/meeting_details.html',context={'meeting_request':meeting_request})
    else:
        return HttpResponseRedirect(reverse('not_found'))




@login_required
def meeting_update(request, meeting_id):
    try:
        meeting_request = MeetingRequests.objects.get(pk=meeting_id)
    except MeetingRequests.DoesNotExist:
        return redirect('not_found')
    if request.method == 'POST':
        form = MeetingRequestUpdateForm(request.POST, instance=meeting_request)
        if form.is_valid():
            form.save()
            return redirect('meeting', meeting_id=meeting_id)
    else:
        form = MeetingRequestUpdateForm(instance=meeting_request)
    
    return render(request, 'dashboard/meetings/meeting_update.html', {'form': form})

@login_required
def calendar_view(request):
    status = request.GET.get('status')  # Get the status parameter from the request
    if status:
        if status == 'all':
            meeting_requests = MeetingRequests.objects.all()
        else:
            meeting_requests = MeetingRequests.objects.filter(status=status)
    else:
        meeting_requests = MeetingRequests.objects.all()  # Fetch all meeting requests
    return render(request, 'dashboard/meetings/meeting_calender.html', {'meeting_requests': meeting_requests})


@login_required
def calendar_data(request):
    status = request.GET.get('status')
    if status:
        if status == 'all':
            meeting_requests = MeetingRequests.objects.all()
        else:
            meeting_requests = MeetingRequests.objects.filter(status=status)
    else:
        meeting_requests = MeetingRequests.objects.all()

    # Serialize meeting requests data
    meeting_data = []
    for meeting in meeting_requests:
        meeting_data.append({
            'meeting_id' : meeting.id,
            'start_up': meeting.start_up.name,
            'vc': meeting.vc.firm_name,
            'meeting_date_time': meeting.meeting_date_time.isoformat(),
            'status': meeting.status
        })

    return JsonResponse(meeting_data, safe=False)
