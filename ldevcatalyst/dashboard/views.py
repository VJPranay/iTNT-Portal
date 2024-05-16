from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from registrations.models import StartUpRegistrations
from django.db.models import Count
from django.contrib import messages
from registrations.models import ResearcherRegistrations,StartUpRegistrations,VCRegistrations
from meetings.models import MeetingRequests

def custom_login(request,):
    if request.user.is_authenticated:
        return redirect('rolls_royce_challenge_details')
    else:
        if request.method == 'POST':
            form = AuthenticationForm(request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    return JsonResponse({'success': True})
                else:
                    return JsonResponse({'success': False})
        elif request.method == 'GET':
            return render(request, 'login.html')
        else:
            return render(request, 'login.html')
    


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))
    




@login_required
def dashboard_index(request):
    # messages.success(request, 'This is a success message.')

    # messages.error(request, 'This is an error message.')

    # messages.info(request, 'This is an info message.')

    # messages.warning(request, 'This is a warning message.')
    sme_count = ResearcherRegistrations.objects.all().count()
    startup_count = StartUpRegistrations.objects.all().count()
    vc_count = VCRegistrations.objects.all().count()
    meeting_count = MeetingRequests.objects.all().count()
    data = {
         'sme_count': sme_count,
         'startup_count': startup_count,
        'vc_count': vc_count,
         'meeting_count': meeting_count
     }
    return render(request,'dashboard/dashboard.html',context=data)



# @login_required
# def dashboard_index(request):
#     # messages.success(request, 'This is a success message.')

#     # messages.error(request, 'This is an error message.')

#     # messages.info(request, 'This is an info message.')

#     # messages.warning(request, 'This is a warning message.')
#     sme_count = ResearcherRegistrations.objects.all().count()
#     startup_count = StartUpRegistrations.objects.all().count()
#     vc_count = VCRegistrations.objects.all().count()
#     meeting_count = MeetingRequests.objects.all().count()
#     data = {
#         'sme_count': sme_count,
#         'startup_count': startup_count,
#         'vc_count': vc_count,
#         'meeting_count': meeting_count
#     }
#     return render(request,'dashboard/dashboard.html',context=data)

