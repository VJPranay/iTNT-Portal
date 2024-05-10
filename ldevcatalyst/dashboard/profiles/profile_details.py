
from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from profiles.models import StartUp


@login_required
def startup_profile_details(request, pk):
    try:
        startup = StartUp.objects.get(pk=pk)
        return render(request, 'dashboard/profiles/v2/startup_profile_details.html', {'startup': startup})
    except StartUp.DoesNotExist:
        return HttpResponseRedirect(reverse('not_found'))
