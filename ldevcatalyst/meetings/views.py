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
from profiles.models import VC ,Student
from .models import MeetingRequests


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
def student_meeting_request(request):
    if request.user.user_role == 4:  # For industry users
        student_id = request.POST.get('student_id', None)
        if student_id is None:
            return JsonResponse({'success': 'false'})
        else:
            try:
                # Here you would handle the meeting request for industry users
                # with the specified student_id
                # Placeholder code to create a new meeting request
                new_meeting_request = MeetingRequests.objects.create(
                    industry_user_id=request.user.id,
                    student_id=student_id,
                    status='pending'
                )
                new_meeting_request.save()
                return JsonResponse({'success': 'true'})
            except Exception as e:
                print(e)
                return JsonResponse({'success': 'false'})
    elif request.user.user_role is None:  # For users without a specific role (e.g., students)
        # Here you would handle the meeting request for students
        # Placeholder code to update the meeting status
        student_id = request.user.id  # Assuming student_id is the user ID for students
        meeting_status = request.POST.get('meeting_status', None)
        if meeting_status is None:
            return JsonResponse({'success': 'false'})
        else:
            try:
                meeting_request = MeetingRequests.objects.get(student_id=student_id, status='pending')
                meeting_request.status = 'accepted' if meeting_status == 'true' else 'rejected'
                meeting_request.save()
                return JsonResponse({'success': 'true'})
            except Exception as e:
                print(e)
                return JsonResponse({'success': 'false'})
    else:
        return JsonResponse({'success': 'false'})

       
@login_required
def fetch_student_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        area_of_interest_id = data.get('area_of_interest_id')
        if not area_of_interest_id:
            return JsonResponse([], safe=False)
        
        # Assuming the industry user's ID is stored in a field named 'user_id'
        industry_profile_id = Industry.objects.get(user_id=request.user.id).id
        industry_meetings_reqests_student_ids = MeetingRequests.objects.filter(industry_id=industry_profile_id, status='pending', student__area_of_interest=area_of_interest_id).values_list('student', flat=True)
        student_profiles = Student.objects.filter(id__in=industry_meetings_reqests_student_ids)
        
        # Prepare data to be sent as JSON response
        profiles_data = []
        for profile in student_profiles:
            profiles_data.append({
                'student_id': profile.id,
                'student_name': profile.name,
                'funding_stage': profile.funding_stage.name,
            })
        return JsonResponse(profiles_data, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)
    
    
@login_required
def fetch_student_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id', None)
        if not student_id:
            return JsonResponse({'error': 'Invalid student ID'}, status=400)
        
        # Fetch student details based on student_id
        student_data = {}
        try:
            student = Student.objects.get(id=student_id)
            student_data['name'] = student.name
            student_data['area_of_interest'] = student.area_of_interest.name
            student_data['year_of_graduation'] = student.year_of_graduation
            student_data['state'] = student.state.name
            student_data['district'] = student.district.name
            student_data['email'] = student.email
            student_data['department'] = student.department.name
            student_data['project_idea'] = student.project_idea
            
        except Student.DoesNotExist:
            return JsonResponse({'error': 'Student not found'}, status=404)

        # Construct HTML for the student details
        html = f"""
           													<!--begin::Profile-->
                                                            <div class="d-flex gap-7 align-items-center">
                                                                <!--begin::Avatar-->
                                                                <div class="symbol symbol-circle symbol-100px">
                                                                    <span class="symbol-label bg-light-success fs-1 fw-bolder">{student.name[:1]}</span>
                                                                </div>
                                                                <!--end::Avatar-->
                                                                <!--begin::Contact details-->
                                                                <div class="d-flex flex-column gap-2">
                                                                    <!--begin::Name-->
                                                                    <h3 class="mb-0">{student.name}</h3>
                                                                    <!--end::Name-->
                                                                    <!--begin::Email-->
                                                                    <div class="d-flex align-items-center gap-2">
                                                                        <i class="ki-outline ki-sms fs-2"></i>
                                                                        <a href="#" class="text-muted text-hover-primary">{student.email}</a>
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
                                                                            <div class="fw-bold fs-5">{student.state.name}</div>
                                                                        </div>
                                                                        <!--end::state-->
                                                                        <!--begin::district-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">District</div>
                                                                            <div class="fw-bold fs-5">{student.district.name}</div>
                                                                        </div>
                                                                        <!--end::district-->
                                                                        <!--begin::department_id-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Department ID</div>
                                                                            <div class="fw-bold fs-5">{student.department.name}</div>
                                                                        </div>
                                                                        <!--end::department_id-->
                                                                        <!--begin::year_of_graduation-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Year of Graduation</div>
                                                                            <div class="fw-bold fs-5">{student.year_of_graduation}</div>
                                                                        </div>
                                                                        <!--end::year_of_graduation-->
                                                                        <!--begin::email-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Email</div>
                                                                            <div class="fw-bold fs-5">{student.email}</div>
                                                                        </div>
                                                                        <!--end::email-->
                                                                        <!--begin::project_idea-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Project Idea</div>
                                                                            <div class="fw-bold fs-5">{student.project_idea}</div>
                                                                        </div>
                                                                        <!--end::project_idea-->
                                                                        <!--begin::area_of_interest_id-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Area of Interest ID</div>
                                                                            <div class="fw-bold fs-5">{student.area_of_interest}</div>
                                                                        </div>
                                                                        <!--end::area_of_interest_id-->
                                                                    </div>
                                                                    <!--end::Additional details-->
                                                                </div>
                                                                <!--end:::Tab pane-->
                                                            </div>
                                                            <!--end::Tab content-->
                """
        # Populate the HTML with student data
        for key, value in student_data.items():
            html += f"""
                <div class="d-flex flex-column gap-1">
                    <div class="fw-bold text-muted">{key.replace('_', ' ').title()}</div>
                    <div class="fw-bold fs-5">{value}</div>
                </div>
            """
        
        # Send the HTML response to the JavaScript function
        return JsonResponse({'html': html})
    else:
        # Handle invalid request
        return JsonResponse({'error': 'Invalid request'}, status=400)
