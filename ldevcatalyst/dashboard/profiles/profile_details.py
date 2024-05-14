
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from profiles.models import StartUp, Researcher, Student, VC, Industry


@login_required
def startup_profile_details(request, pk):
    try:
        startup = StartUp.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/startup_profile_details.html', {'startup': startup})
    except StartUp.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
    

@login_required
def researcher_profile_details(request, pk):
    try:
        researcher = Researcher.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/researcher_profile_details.html', {'researcher': researcher})
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
    
