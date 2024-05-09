from registrations.models import VCRegistrations
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



@login_required
def vc_overview(request):
    # VC count by district
    vc_count_by_district = VCRegistrations.objects.values('district__name').annotate(vc_count=Count('id')).order_by('-vc_count')
    by_district = []
    for item in vc_count_by_district:
        by_district.append({
            'district__name': item['district__name'],
            'vc_count': item['vc_count'],
        })

    # VC count by area of interest
    vc_count_by_interest = VCRegistrations.objects.values('area_of_interest__name').annotate(vc_count=Count('id')).order_by('-vc_count')
    by_interest = []
    for item in vc_count_by_interest:
        by_interest.append({
            'area_of_interest__name': item['area_of_interest__name'],
            'vc_count': item['vc_count'],
        })

    # VC count by funding stage
    vc_count_by_stage = VCRegistrations.objects.values('funding_stage__name').annotate(vc_count=Count('id')).order_by('-vc_count')
    by_stage = []
    for item in vc_count_by_stage:
        by_stage.append({
            'funding_stage__name': item['funding_stage__name'],
            'vc_count': item['vc_count'],
        })

    counts = {
        'vc_count': VCRegistrations.objects.all().count()
    }

    return render(request, 'dashboard/reports/vc/overview.html', context={
        'counts': counts,
        'district_data': by_district,
        'interest_data': by_interest,
        'stage_data': by_stage,
    })
