
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from registrations.models import StartUpRegistrations,ResearcherRegistrations, StudentRegistrations


@login_required
def startup_registration_details(request, pk):
    try:
        startup = StartUpRegistrations.objects.get(pk=pk)
        return render(request, 'dashboard/registrations/v2/startup_registration_details.html', {'startup': startup})
    except StartUpRegistrations.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))




@login_required
def Researcher_registration_details(request, pk):
    try:
        researcher = ResearcherRegistrations.objects.get(pk=pk)
        return render(request, 'dashboard/registrations/v2/researcher_registration_details.html', {'researcher': researcher})
    except ResearcherRegistrations.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))




@login_required
def student_registration_details(request, pk):
    try:
        student = StudentRegistrations.objects.get(pk=pk)
        return render(request, 'dashboard/registrations/v2/student_registration_details.html', {'student': student})
    except StudentRegistrations.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))



