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
def startup_overview(request):
    startup_count_by_interest = StartUpRegistrations.objects.values('area_of_interest__name').annotate(startup_count=Count('id')).order_by('-startup_count')
    by_area_of_interest = []
    for item in startup_count_by_interest:
        by_area_of_interest.append({ 
            'area_of_interest__name' : item['area_of_interest__name'],
            'startup_count' : item['startup_count'], 
        })
    startup_count_by_district = StartUpRegistrations.objects.values('district__name').annotate(startup_count=Count('id')).order_by('-startup_count')
    by_district = []
    for item in startup_count_by_district:
        by_district.append({
            'district__name' : item['district__name'],
            'startup_count' : item['startup_count'],
        })
    startup_count_by_preferred_investment_stage = StartUpRegistrations.objects.values('preferred_investment_stage__name').annotate(startup_count=Count('id')).order_by('-startup_count')
    by_preferred_investment_stage = []
    for item in startup_count_by_preferred_investment_stage:
        by_preferred_investment_stage.append({
            'preferred_investment_stage__name' : item['preferred_investment_stage__name'],
            'startup_count' : item['startup_count'],
        })

    counts ={
        'startup_count' : StartUpRegistrations.objects.all().count()
    }
    return render(request,'dashboard/reports/startup_overview.html',context={
        'counts' :counts,
        'area_of_interest_data' : by_area_of_interest,
        'district_data' : by_district,
        'preferred_investment_stage_data' : by_preferred_investment_stage,
    })

