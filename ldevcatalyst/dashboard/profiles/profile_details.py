
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from profiles.models import StartUp, Researcher, Student, VC, Industry
from smeconnect.models import MeetingRequest


@login_required
def startup_profile_details(request, pk):
    print(pk)
    try:
        startup = StartUp.objects.get(pk=pk)
        check_meetings = MeetingRequest.objects.filter(sender_id=request.user.id,receiver_id=startup.user.id)
        print(request.user.user_role)
        print(check_meetings.count())
        meeting_exists = 'false'
        for x in check_meetings:
            if x.status == 'sent' or x.status == 'accepted':
                meeting_exists = 'true'
        return render(request, 'dashboard/profiles/v2/startup_profile_details.html', {'startup': startup,'meeting_exists': meeting_exists})
    except StartUp.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    

@login_required
def researcher_profile_details(request, pk):
    try:
        researcher = Researcher.objects.get(pk=pk)
        check_meetings = MeetingRequest.objects.filter(sender_id=request.user.id,receiver_id=researcher.user.id)
        meeting_exists = 'false'
        for x in check_meetings:
            if x.status == 'sent' or x.status == 'accepted':
                meeting_exists = 'true'
        return render(request, 'dashboard/profiles/v2/researcher_profile_details.html', 
                      {
                          'researcher': researcher,
                          'meeting_exists': meeting_exists,
                        })
    except Researcher.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    

@login_required
def student_profile_details(request, pk):
    try:
        student = Student.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/student_profile_details.html', {'student': student})
    except Student.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    


@login_required
def vc_profile_details(request, pk):
    try:
        vc = VC.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/vc_profile_details.html', {'vc': vc})
    except VC.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    


@login_required
def industry_profile_details(request, pk):
    try:
        industry = Industry.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/industry_profile_details.html', {'industry': industry})
    except Industry.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    
