from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.http import JsonResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout as auth_logout
from django.urls import reverse
from django.http import HttpResponseNotAllowed
from registrations.models import IndustryRegistrations
from django.db.models import Count
from django.contrib import messages



@login_required
def industry_overview(request):
    industry_count_by_interest = IndustryRegistrations.objects.values('area_of_interest__name').annotate(industry_count=Count('id')).order_by('-industry_count')
    by_area_of_interest = []
    for item in industry_count_by_interest:
        by_area_of_interest.append({ 
            'area_of_interest__name' : item['area_of_interest__name'],
            'industry_count' : item['industry_count'], 
        })
    industry_count_by_district = IndustryRegistrations.objects.values('district__name').annotate(industry_count=Count('id')).order_by('-industry_count')
    by_district = []
    for item in industry_count_by_district:
        by_district.append({
            'district__name' : item['district__name'],
            'industry_count' : item['industry_count'],
        })
    

    counts ={
        'industry_count' : IndustryRegistrations.objects.all().count()
    }
    return render(request,'dashboard/reports/industry/industry_overview.html',context={
        'counts' :counts,
        'area_of_interest_data' : by_area_of_interest,
        'district_data' : by_district,
       
    })

