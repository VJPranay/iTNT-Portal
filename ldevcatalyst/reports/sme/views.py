from django.db.models import Count, Case, When, Value, CharField
from django.shortcuts import render
from registrations.models import ResearcherRegistrations, AreaOfInterest, PatentInfo, District, Institution
from django.contrib.auth.decorators import login_required

@login_required
def researcher_overview(request):
    # Get approved area of interest categories and their counts
    approved_categories = AreaOfInterest.get_approved_categories()
    researcher_count_by_interest = ResearcherRegistrations.objects.filter(area_of_interest__in=approved_categories).values('area_of_interest__name').annotate(researcher_count=Count('id')).order_by('-researcher_count')

    # Get counts for other area of interest categories
    other_interest_count = ResearcherRegistrations.objects.exclude(area_of_interest__in=approved_categories).aggregate(count=Count('id'))['count'] or 0

    # Combine approved categories and count into a list
    by_area_of_interest = []
    for item in researcher_count_by_interest:
        by_area_of_interest.append({ 
            'area_of_interest__name': item['area_of_interest__name'],
            'researcher_count': item['researcher_count'], 
        })
    
    # Add "Others" category with its count to the list
    by_area_of_interest.append({
        'area_of_interest__name': 'Others',
        'researcher_count': other_interest_count,
    })

    # Researcher count by district
    researcher_count_by_district = ResearcherRegistrations.objects.filter(district__isnull=False).values('district__name').annotate(researcher_count=Count('id')).filter(researcher_count__gt=0).order_by('-researcher_count')
    by_district = []
    for item in researcher_count_by_district:
        by_district.append({
            'district__name': item['district__name'],
            'researcher_count': item['researcher_count'],
        })

    # Researcher count by institution
    researcher_count_by_institution_above_20 = Institution.objects.annotate(researcher_count=Count('researcherregistrations')).filter(researcher_count__gt=20).order_by('-researcher_count')
    institutions_above_20 = []
    for item in researcher_count_by_institution_above_20:
        institutions_above_20.append({
            'institution__name': item.name,
            'researcher_count': item.researcher_count,
        })

    other_institution_count = Institution.objects.annotate(researcher_count=Count('researcherregistrations')).filter(researcher_count__lte=20).aggregate(total_count=Count('id'))
    other_institutions = [{
        'institution__name': 'Other Institutions',
        'researcher_count': other_institution_count['total_count'],
    }]

    counts = {
        'researcher_count': ResearcherRegistrations.objects.all().count(),
    }
    return render(request, 'dashboard/reports/sme/overview.html', context={
        'counts': counts,
        'area_of_interest_data': by_area_of_interest,
        'district_data': by_district,
        'institutions_above_20': institutions_above_20,
        'other_institutions': other_institutions,
    })
