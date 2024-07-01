from django.shortcuts import render,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
import random
from profiles.models import StartUp
from .models import MeetingRequests
from smeconnect.models import MeetingRequest
from vcstartup_meetings.models import vcstartup_MeetingRequest
from django.db.models import Count
from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json
from profiles.models import VC ,Student,Industry
from smeindustryconnect.models import SmeIndustryMeetingRequest
from mentorstartupconnect.models import MentorStartupMeetingRequest
#from .models import MeetingRequests
from django.utils.html import escape
from .forms import MeetingRequestUpdateForm,VCMeetingRequestAcceptForm
from django.http import JsonResponse


# Create your views here.
@login_required
def vc_meeting_requests(request):
    if request.user.user_role ==  8:
        vc_profile_id = VC.objects.get(user_id=request.user.id).id
        template_data = {
            'interest_areas_data' : MeetingRequests.objects.filter(vc_id=vc_profile_id,status='start_up_request').values('start_up__area_of_interest__id', 'start_up__area_of_interest__name').annotate(requests_count=Count('id')),
            'start_up_profiles' : []
        }
        print(template_data)
        return render(request,'dashboard/meetings/vc/meeting_requests.html',context=template_data)
    else:
        return HttpResponseRedirect(reverse('not_found'))

@login_required
def fetch_startup_profiles(request):
    if request.user.user_role ==  8:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            area_of_interest_id = data.get('area_of_interest_id')
            if not area_of_interest_id:
                return JsonResponse([], safe=False)
            vc_profile_id = VC.objects.get(user_id=request.user.id).id
            vc_meetings_reqests_startup_ids = MeetingRequests.objects.filter(vc_id=vc_profile_id, status='start_up_request', start_up__area_of_interest=area_of_interest_id).values_list('start_up', flat=True)
            startup_profiles = StartUp.objects.filter(id__in=vc_meetings_reqests_startup_ids)
            # Prepare data to be sent as JSON response
            profiles_data = []
            for profile in startup_profiles:
                profiles_data.append({
                    'startup_id': profile.id,
                    'startup_name': profile.company_name,
                    'funding_stage': 'N / A' if not profile.fund_raised else profile.fund_raised.name,
                })
            return JsonResponse(profiles_data, safe=False)
        else:
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return HttpResponseRedirect(reverse('not_found'))
    
    
@login_required
def fetch_startup_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        startup_id = data.get('startup_id',None)
        if not startup_id:
            return JsonResponse({'error': 'Invalid startup ID'}, status=400)
        # Fetch startup details based on startup_id
        try:
            startup = StartUp.objects.get(id=startup_id)
        except StartUp.DoesNotExist:
            return JsonResponse({'error': 'Invalid startup ID'}, status=400)

        # # get meeting details
        # try:
        #     meeting_info = MeetingRequests.objects.get(vc__user_id=request.user.id, start_up_id=startup)
        # except MeetingRequests.DoesNotExist:
        #     print('invalid request here ')
        #     return JsonResponse({'error': 'Invalid startup/vc ID'}, status=400)
        
        try:
            meeting_info = MeetingRequests.objects.get(vc__user_id=request.user.id, start_up_id=startup)
            meeting_buttons_html = f"""
                <div style="margin: 20px;display: flex;">
                    <a href="{reverse('vc_meeting_accept', kwargs={'meeting_id': meeting_info.id})}" id="acceptMeetingRequest" class="btn btn-sm btn-success btn-active-light-success" style="margin: 10px;">Accept meeting request</a>
                    <a href="{reverse('vc_meeting_reject', kwargs={'meeting_id': meeting_info.id})}" id="rejectMeetingRequest" class="btn btn-sm btn-danger btn-active-light-danger" style="margin: 10px;">Deny</a>
                </div>
            """
        except MeetingRequests.DoesNotExist:
            meeting_buttons_html = ""
        
        pitch_deck_url  = None
            
        if startup.pitch_deck:
            pitch_deck_url = startup.pitch_deck.url
            
            
        

        # Construct HTML for the startup details
        html = f"""
            <!--begin::Profile-->
            <div class="d-flex gap-7 align-items-center" id="startup-id" data-startup-id="{startup.id}">
                <!--begin::Avatar-->
                <div class="symbol symbol-circle symbol-100px">
                    <span class="symbol-label bg-light-success fs-1 fw-bolder">{startup.company_name[:1]}</span>
                </div>
                <!--end::Avatar-->
                <!--begin::Contact details-->
                <div class="d-flex flex-column gap-2">
                    <!--begin::Name-->
                    <h3 class="mb-0">{startup.company_name}</h3>
                    <!--end::Name-->
                    <!--begin::Email-->
                    <div class="d-flex align-items-center gap-2">
                        <i class="ki-outline ki-sms fs-2"></i>
                        <a href="#" class="text-muted text-hover-primary">{startup.area_of_interest.name if startup.area_of_interest else None}</a>
                    </div>
                    <!--end::Email-->
                    <!--begin::Phone-->
                    <div class="d-flex align-items-center gap-2">
                        <i class="ki-outline ki-phone fs-2"></i>
                        <a href="#" class="text-muted text-hover-primary">{startup.fund_raised.name if startup.fund_raised else None}</a>
                    </div>
                    <!--end::Phone-->
                </div>
                <!--end::Contact details-->
            </div>
            {meeting_buttons_html}
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
                            <div class="fw-bold text-muted">Pitch Desk</div>
                            <a href="{pitch_deck_url}" class="fw-bold fs-5">{startup.pitch_deck}</a>
                        </div>
                        
                        <!--end::Company description-->
                        <!--begin::dpiit number-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">DPIIT number</div>
                            <div class="fw-bold fs-5">{startup.dpiit_number}</div>
                        </div>
                        <!--end::dpiit number-->
                        <!--begin::Website-->
                        <!--end::=Website-->
                        
                        <!--begin::market_size-->
                        <!--end::market_size-->
                        <!--begin::funding_stage-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">Current funding stage</div>
                            <div class="fw-bold fs-5">{startup.fund_raised.name if startup.fund_raised else None}</div>
                        </div>
                        <!--end::funding_stage-->
                        <!--begin::area_of_interest-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">Industry</div>
                            <div class="fw-bold fs-5">{startup.area_of_interest.name if startup.area_of_interest else None}</div>
                        </div>
                        <!--end::area_of_interest-->
                        <!--begin::area_of_interest-->
                        <!--end::area_of_interest-->
                        <!--begin::area_of_interest-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">Founding year</div>
                            <div class="fw-bold fs-5">{startup.year_of_establishment}</div>
                        </div>
                        <!--end::area_of_interest-->
                        <!--begin::area_of_interest-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">Co-Founder team size </div>
                            <div class="fw-bold fs-5">{startup.co_founders_count}</div>
                        </div>
                        <!--end::area_of_interest-->
                        <!--begin::area_of_interest-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">Total team size</div>
                            <div class="fw-bold fs-5">{startup.team_size}</div>
                        </div>
                        <!--end::area_of_interest-->
                        <!--begin::area_of_interest-->
                        <!--end::area_of_interest-->
                        <!--begin::area_of_interest-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">State</div>
                            <div class="fw-bold fs-5">{startup.state.name if startup.state else None}</div>
                        </div>
                        <!--end::area_of_interest-->
                        <!--begin::district-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">City</div>
                            <div class="fw-bold fs-5">{startup.district.name if startup.district else None}</div>
                        </div>
                        <!--end::district-->
                        <div class="d-flex flex-column gap-1">
                            <div class="fw-bold text-muted">Full Video</div>
                            <a href="{startup.video_link}" class="fw-bold fs-5">{startup.video_link}</a>
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
                    check_meeting = MeetingRequests.objects.get(start_up_id=startup_id, vc_id=vc_info.id, status='start_up_request')
                    return JsonResponse({'success': 'false'})
                except MeetingRequests.DoesNotExist:
                    new_meeting_request = MeetingRequests.objects.create(
                        start_up_id=startup_id,
                        vc_id=vc_info.id,
                        status='start_up_request'
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
                check_meeting = MeetingRequests.objects.get(start_up_id=startup_id,vc_id=vc_id, status='start_up_request')
                check_meeting.status = 'accepted' if meeting_status else 'rejected'
                check_meeting.save()
                return JsonResponse({'success': 'true'})
            except MeetingRequests.DoesNotExist:
                return JsonResponse({'success': 'false'})
    else:
        return JsonResponse({'success': 'false'})
    
    

@login_required
def meetings(request,meeting_status=None):
    if request.user.user_role in [1,2,3,6,8]: 
        query = {
        
        }
        if meeting_status:
            query['status'] = meeting_status
        if request.user.user_role == 6:
            query['start_up__user__id'] = request.user.id
        if request.user.user_role == 8:
            query['vc__user__id'] = request.user.id
        meeting_requests = MeetingRequests.objects.filter(**query)
        meeting_requests_list = []
        for x in meeting_requests:
            temp = {
                'meeting_id' : x.id,
                'start_up':x.start_up.company_name,
                'vc' : x.vc.firm_name,
                'created' : x.created,
                'updated':x.updated,
            }
            meeting_requests_list.append(temp)
        return render(request, 'dashboard/meetings/list.html',context={'meeting_requests':meeting_requests_list})
    else:
        return HttpResponseRedirect(reverse('not_found'))

@login_required
def meeting(request, meeting_id=None):
    if request.user.user_role in [1, 2, 3, 4, 5, 6, 8, 9] and meeting_id is not None: 
        try:
            if request.user.user_role == 6:  # Startup
                try:
                    meeting_request = vcstartup_MeetingRequest.objects.get(id=meeting_id, start_up__user__id=request.user.id)
                except vcstartup_MeetingRequest.DoesNotExist:
                    meeting_request = MeetingRequests.objects.get(id=meeting_id, sme__user__id=request.user.id)

            elif request.user.user_role == 5:  # SME
                try:
                    meeting_request = MeetingRequests.objects.get(id=meeting_id, sme__user__id=request.user.id)
                except MeetingRequests.DoesNotExist:
                    meeting_request = SmeIndustryMeetingRequest.objects.get(id=meeting_id, sme__user__id=request.user.id)

            elif request.user.user_role == 8:  # VC
                meeting_request = vcstartup_MeetingRequest.objects.get(id=meeting_id, vc__user__id=request.user.id)

            elif request.user.user_role == 9:  # Mentor
                meeting_request = MentorStartupMeetingRequest.objects.get(id=meeting_id, mentor__user__id=request.user.id)

            elif request.user.user_role == 4:  # Industry
                meeting_request = SmeIndustryMeetingRequest.objects.get(id=meeting_id, industry__user__id=request.user.id)

            else:  # Admins or other roles
                meeting_request = MeetingRequests.objects.get(id=meeting_id)

            return render(request, 'dashboard/meetings/meeting_details.html', context={'meeting_request': meeting_request})

        except (MeetingRequests.DoesNotExist, vcstartup_MeetingRequest.DoesNotExist, 
                MentorStartupMeetingRequest.DoesNotExist, SmeIndustryMeetingRequest.DoesNotExist):
            return redirect('not_found')
    else:
        return HttpResponseRedirect(reverse('not_found'))


    

# start up send requests to VC
# vc accept request with meeting type , date , time 
# start up confirms meeting
# admin adds link ( optional )
# admin confirms reschedule
    

@login_required
def vc_meeting_accept(request, meeting_id):
    try:
        meeting_request = MeetingRequests.objects.get(pk=meeting_id, vc__user_id=request.user.id, status='start_up_request')
    except MeetingRequests.DoesNotExist:
        return redirect('not_found')

    if request.method == 'POST':
        form = VCMeetingRequestAcceptForm(request.POST, instance=meeting_request)
        if form.is_valid():
            form.save()
            meeting_info = MeetingRequests.objects.get(id=meeting_id)
            meeting_info.status = 'vc_accepted'
            meeting_info.save()
            return redirect('meeting', meeting_id=meeting_id)
    else:
        form = VCMeetingRequestAcceptForm(instance=meeting_request)
    return render(request, 'dashboard/meetings/vc/meeting_accept.html', {'form': form, 'meeting_request': meeting_request})




@login_required
def vc_meeting_reject(request, meeting_id):
    try:
        meeting_request = MeetingRequests.objects.get(pk=meeting_id, vc__user_id=request.user.id, status='start_up_request')
    except MeetingRequests.DoesNotExist:
        return redirect('not_found')

    if request.method == 'POST':
        form = VCMeetingRequestAcceptForm(request.POST, instance=meeting_request)
        if form.is_valid():
            meeting_request = form.save(commit=False)
            meeting_request.status = 'rejected'
            meeting_request.cancellation_reason = form.cleaned_data.get('cancellation_reason')
            meeting_request.save()
            
            if hasattr(request.user, 'profile') and request.user.profile.is_vc:
                return redirect('vc_profiles_list')  # Update with actual URL name for VC profiles
            else:
                return redirect('startup_profiles_list')  # Update with actual URL name for Startup profiles

    else:
        form = VCMeetingRequestAcceptForm(instance=meeting_request)

    return render(request, 'dashboard/meetings/vc/meeting_reject.html', {'form': form, 'meeting_request': meeting_request})



@login_required
def meeting_update(request, meeting_id):
    if request.user.user_role in [1,2,3,6,8] or meeting_id is not None: 
        if request.method == 'GET':
            try:
                if request.user.user_role == 6:
                    meeting_request = MeetingRequests.objects.get(pk=meeting_id,start_up__user__id=request.user.id)
                elif request.user.user_role == 8:
                    meeting_request = MeetingRequests.objects.get(pk=meeting_id,vc__user__id=request.user.id)
                else:
                    meeting_request = MeetingRequests.objects.get(pk=meeting_id)
                form = MeetingRequestUpdateForm(instance=meeting_request)
                return render(request, 'dashboard/meetings/meeting_update.html', {'form': form,'meeting_request':meeting_request})
            except MeetingRequests.DoesNotExist:
                return redirect('not_found')
        if request.method == 'POST':
            if request.user.user_role == 6:
                meeting_request = MeetingRequests.objects.get(pk=meeting_id,start_up__user__id=request.user.id)
            elif request.user.user_role == 8:
                meeting_request = MeetingRequests.objects.get(pk=meeting_id,vc__user__id=request.user.id)          
                form = MeetingRequestUpdateForm(request.POST, instance=meeting_request)
                if form.is_valid():
                    form.status == 'vc_accepted'
                    form.save()
                    return redirect('meeting', meeting_id=meeting_id)
            elif request.user.user_role in [1,2,3]:
                meeting_request = MeetingRequests.objects.get(pk=meeting_id)
                form = MeetingRequestUpdateForm(request.POST, instance=meeting_request)
                if form.is_valid():
                    form.save()
                    if meeting_request.status == 'online_meeting_link_awaiting' or meeting_request.status == 'start_up_reschedule':
                        meeting_request.status = 'scheduled'
                        meeting_request.save()
                    return redirect('meeting', meeting_id=meeting_id)
            else:
                meeting_request = MeetingRequests.objects.get(pk=meeting_id)
        else:
            form = MeetingRequestUpdateForm(instance=meeting_request)
        return render(request, 'dashboard/meetings/meeting_update.html', {'form': form})
    else:
        return HttpResponseRedirect(reverse('not_found'))

# @login_required
# def calendar_view(request):
#     status = request.GET.get('status')  # Get the status parameter from the request
#     if status:
#         if status == 'all':
#             meeting_requests = MeetingRequest.objects.all()
#         else:
#             meeting_requests = MeetingRequest.objects.filter(status=status)
#     else:
#         meeting_requests = MeetingRequest.objects.all()  # Fetch all meeting requests
#     return render(request, 'dashboard/meetings/meeting_calender.html', {'meeting_requests': meeting_requests})

@login_required
def calendar_view(request):
    status = request.GET.get('status')

    # Initialize variables for all types of meeting requests
    meeting_requests = {
        'smeconnect': MeetingRequest.objects.all(),
        'vc': vcstartup_MeetingRequest.objects.all(),
        'mentor': MentorStartupMeetingRequest.objects.all(),
        'sme_industry': SmeIndustryMeetingRequest.objects.all(),
    }

    if status:
        if status != 'all':
            meeting_requests['smeconnect'] = MeetingRequest.objects.filter(status=status)
            meeting_requests['vc'] = vcstartup_MeetingRequest.objects.filter(status=status)
            meeting_requests['mentor'] = MentorStartupMeetingRequest.objects.filter(status=status)
            meeting_requests['sme_industry'] = SmeIndustryMeetingRequest.objects.filter(status=status)

    return render(request, 'dashboard/meetings/meeting_calender.html', context={'meeting_request': meeting_requests})

@login_required
def calendar_data(request):
    status = request.GET.get('status', 'all')  # Default status to 'all' if not provided

    # Fetch all meeting requests based on status filter
    if status != 'all':
        meeting_requests_vcstartup = vcstartup_MeetingRequest.objects.filter(status=status)
        meeting_requests_sme = MeetingRequest.objects.filter(status=status)
        meeting_requests_mentor = MentorStartupMeetingRequest.objects.filter(status=status)
        meeting_requests_industry = SmeIndustryMeetingRequest.objects.filter(status=status)
    else:
        meeting_requests_vcstartup = vcstartup_MeetingRequest.objects.all()
        meeting_requests_sme = MeetingRequest.objects.all()
        meeting_requests_mentor = MentorStartupMeetingRequest.objects.all()
        meeting_requests_industry = SmeIndustryMeetingRequest.objects.all()

    # Serialize meeting requests data
    meeting_data = []

    # Process vcstartup_MeetingRequest instances
    for meeting in meeting_requests_vcstartup:
        if meeting.date and meeting.time:
            if meeting.sender.user_role == 6:  # startup
                sent_by = 'startup'
                start_up = meeting.sender.username
                vc_name = meeting.receiver.username
            elif meeting.sender.user_role == 8:  # vc
                sent_by = 'vc'
                start_up = meeting.receiver.username
                vc_name = meeting.sender.username
            else:
                continue

            meeting_data.append({
                'meeting_id': meeting.id,
                'start_up': start_up,
                'vc_name': vc_name,
                'meeting_date': meeting.date.strftime('%Y-%m-%d'),
                'meeting_time': meeting.time.strftime('%H:%M'),
                'status': meeting.status,
                'sent_by': sent_by
            })
    
    # Process MeetingRequest instances
    for meeting in meeting_requests_sme:
        if meeting.date and meeting.time:
            if meeting.sender.user_role == 6:  # startup
                sent_by = 'startup'
                start_up = meeting.sender.username
                sme_name = meeting.receiver.username
            elif meeting.receiver.user_role == 5:  # sme
                sent_by = 'sme'
                start_up = meeting.receiver.username
                sme_name = meeting.sender.username
            else:
                continue

            meeting_data.append({
                'meeting_id': meeting.id,
                'start_up': start_up,
                'sme_name': sme_name,
                'meeting_date': meeting.date.strftime('%Y-%m-%d'),
                'meeting_time': meeting.time.strftime('%H:%M'),
                'status': meeting.status,
                'sent_by': sent_by
            })
    
    # Process MentorStartupMeetingRequest instances
    for meeting in meeting_requests_mentor:
        if meeting.date and meeting.time:
            if meeting.sender.user_role == 6:  # startup
                sent_by = 'startup'
                start_up = meeting.sender.username
                mentor_name = meeting.receiver.username
            elif meeting.sender.user_role == 9:  # mentor
                sent_by = 'mentor'
                start_up = meeting.receiver.username
                mentor_name = meeting.sender.username
            else:
                continue

            meeting_data.append({
                'meeting_id': meeting.id,
                'start_up': start_up,
                'mentor_name': mentor_name,
                'meeting_date': meeting.date.strftime('%Y-%m-%d'),
                'meeting_time': meeting.time.strftime('%H:%M'),
                'status': meeting.status,
                'sent_by': sent_by
            })

    # Process SmeIndustryMeetingRequest instances
    for meeting in meeting_requests_industry:
        if meeting.date and meeting.time:
            if meeting.sender.user_role == 5:  # researcher (sme)
                sent_by = 'sme'
                sme_name = meeting.sender.username
                industry_name = meeting.receiver.username
            elif meeting.sender.user_role == 4:  # industry
                sent_by = 'industry'
                sme_name = meeting.receiver.username
                industry_name = meeting.sender.username
            else:
                continue

            meeting_data.append({
                'meeting_id': meeting.id,
                'sme_name': sme_name,
                'industry_name': industry_name,
                'meeting_date': meeting.date.strftime('%Y-%m-%d'),
                'meeting_time': meeting.time.strftime('%H:%M'),
                'status': meeting.status,
                'sent_by': sent_by
            })

    return JsonResponse(meeting_data, safe=False)

@login_required
def startup_confirm_meeting(request):
    if request.method == 'POST':
        meeting_id = request.POST.get('meeting_id')
        meeting = MeetingRequests.objects.get(pk=meeting_id)
        meeting.status = 'scheduled' if meeting.meeting_type == 'offline' else 'online_meeting_link_awaiting'
        meeting.save()
        return JsonResponse({'message': 'Meeting confirmed successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    
@login_required
def startup_reject_meeting(request):
    if request.method == 'POST':
        meeting_id = request.POST.get('meeting_id')
        meeting = MeetingRequests.objects.get(pk=meeting_id)
        meeting.status = 'rejected'
        meeting.save()
        return JsonResponse({'message': 'Meeting rejected successfully'}, status=200)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    

from django.http import Http404
from django.db.models import Q

@login_required
def meeting_details(request, pk):
    meeting_request = None

    # sme_query = Q(sender__username__icontains='SURG') | Q(sender__username__icontains='RCRG')
    # vc_startup_query = {Q(sender__username__istartswith='VCRG') | Q(sender__username__istartswith='SURG')}
    # mentor_startup_query = {Q(sender__username__istartswith='MNRG') | Q(sender__username__istartswith='RCRG')}
    # sme_industry_query = {Q(sender__username__istartswith='RCRG') | Q(sender__username__istartswith='INRG')}

    # try:
    #     if MeetingRequest.objects.filter(pk=pk).exists():
    #         meeting_request = get_object_or_404(MeetingRequest, pk=pk)
    #     elif vcstartup_MeetingRequest.objects.filter(pk=pk).exists():
    #         meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk)
            
    #     elif MentorStartupMeetingRequest.objects.filter(pk=pk).exists():
    #         meeting_request = get_object_or_404(MentorStartupMeetingRequest, pk=pk)
    #         print("MentorStartupMeetingRequest:", meeting_request)

    #     elif SmeIndustryMeetingRequest.objects.filter(pk=pk).exists():
    #         meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk)
    #         print("SmeIndustryMeetingRequest:", meeting_request)

    #     elif meeting_request is None:
    #         raise Http404("Meeting request not found")
    # except Exception as e:
    #     # Handle other exceptions
    #     print(e)

    # context = {'meeting_request': meeting_request}
    # print(f"meeting_request: {meeting_request}")

    # testing the view here
    try:
        # if MeetingRequest.objects.filter(pk=pk).filter(Q(sender__username__istartswith='SURG') | Q(sender__username__istartswith='RCRG')).exists():
        #     meeting_request = get_object_or_404(MeetingRequest, pk=pk)
        #     print('sme connect --> ', pk)
        # elif vcstartup_MeetingRequest.objects.filter(pk=pk).filter(Q(sender__istartswith='VCRG') | Q(sender__istartswith='SURG')).exists():
        #     meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk)
        #     print('vcstartup MeetingRequest --> ', pk)
            
        # elif MentorStartupMeetingRequest.objects.filter(pk=pk).filter(Q(sender__istartswith='MNRG') | Q(sender__istartswith='RCRG')).exists():
        #     meeting_request = get_object_or_404(MentorStartupMeetingRequest, pk=pk)
        #     print("MentorStartupMeetingRequest:", meeting_request)
        # elif SmeIndustryMeetingRequest.objects.filter(pk=pk).filter(Q(sender__istartswith='RCRG') | Q(sender__istartswith='INRG')).exists():
        #     meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk)
        #     print("SmeIndustryMeetingRequest:", meeting_request)
        if MeetingRequest.objects.filter(pk=pk).filter(Q(sender__username__icontains='SURG') | Q(sender__username__icontains='RCRG')).exists():
            meeting_request = get_object_or_404(MeetingRequest, pk=pk)
            print('sme connect --> ', pk)
        elif vcstartup_MeetingRequest.objects.filter(pk=pk).filter(Q(sender__username__icontains='VCRG') | Q(sender__username__icontains='SURG')).exists():
            meeting_request = get_object_or_404(vcstartup_MeetingRequest, pk=pk)
            print('vcstartup MeetingRequest --> ', pk)
            
        elif MentorStartupMeetingRequest.objects.filter(pk=pk).filter(Q(sender__username__icontains='MNRG') | Q(sender__username__icontains='RCRG')).exists():
            meeting_request = get_object_or_404(MentorStartupMeetingRequest, pk=pk)
            print("MentorStartupMeetingRequest:", meeting_request)
        elif SmeIndustryMeetingRequest.objects.filter(pk=pk).filter(Q(sender__username__icontains='RCRG') | Q(sender__username__icontains='INRG')).exists():
            meeting_request = get_object_or_404(SmeIndustryMeetingRequest, pk=pk)
            print("SmeIndustryMeetingRequest:", meeting_request)
        elif meeting_request is None:
            raise Http404("Meeting request not found")
    except Exception as e:
        # Handle other exceptions
        print(e)

    context = {'meeting_request': meeting_request}

    return render(request, 'dashboard/meetings/meeting_request_details.html', context=context)
