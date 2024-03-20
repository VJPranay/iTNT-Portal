from django.db.models import Count
from django.shortcuts import render
from registrations.models import ResearcherRegistrations, AreaOfInterest, PatentInfo, District, Institution
from django.contrib.auth.decorators import login_required

@login_required
def researcher_overview(request):
    researcher_count_by_interest = ResearcherRegistrations.objects.filter(area_of_interest__isnull=False).values('area_of_interest__name').annotate(researcher_count=Count('id')).filter(researcher_count__gt=0).order_by('-researcher_count')
    by_area_of_interest = []
    for item in researcher_count_by_interest:
        by_area_of_interest.append({ 
            'area_of_interest__name': item['area_of_interest__name'],
            'researcher_count': item['researcher_count'], 
        })

    researcher_count_by_district = ResearcherRegistrations.objects.filter(district__isnull=False).values('district__name').annotate(researcher_count=Count('id')).filter(researcher_count__gt=0).order_by('-researcher_count')
    by_district = []
    for item in researcher_count_by_district:
        by_district.append({
            'district__name': item['district__name'],
            'researcher_count': item['researcher_count'],
        })

    researcher_count_by_institution = Institution.objects.filter(researcherregistrations__isnull=False).values('name').annotate(researcher_count=Count('researcherregistrations')).filter(researcher_count__gt=0).order_by('-researcher_count')
    by_institution = []
    for item in researcher_count_by_institution:
        by_institution.append({
            'institution__name': item['name'],
            'researcher_count': item['researcher_count'],
        })

    counts = {
        'researcher_count': ResearcherRegistrations.objects.all().count(),
    }
    return render(request, 'dashboard/reports/sme/overview.html', context={
        'counts': counts,
        'area_of_interest_data': by_area_of_interest,
        'district_data': by_district,
        'institution_data': by_institution,
    })
