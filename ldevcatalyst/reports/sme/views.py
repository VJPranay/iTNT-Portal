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

    # Combine approved categories and count into a list for area of interest
    by_area_of_interest = []
    for item in researcher_count_by_interest:
        by_area_of_interest.append({ 
            'area_of_interest__name': item['area_of_interest__name'],
            'researcher_count': item['researcher_count'], 
        })
    
    # Add "Others" category with its count to the list for area of interest
    by_area_of_interest.append({
        'area_of_interest__name': 'Others',
        'researcher_count': other_interest_count,
    })

    # Get counts for districts with researcher counts greater than 0
    researcher_count_by_district = ResearcherRegistrations.objects.filter(district__isnull=False).values('district__name').annotate(researcher_count=Count('id')).filter(researcher_count__gt=0).order_by('-researcher_count')
    by_district = []
    for item in researcher_count_by_district:
        by_district.append({
            'district__name': item['district__name'],
            'researcher_count': item['researcher_count'],
        })

    # Get counts for institutions with researcher counts above 20
    institutions_above_20 = Institution.objects.annotate(
        researcher_count=Count('researcherregistrations')
    ).filter(researcher_count__gt=20).values('name', 'researcher_count').order_by('-researcher_count')

    # Get count for other institutions
    other_institutions_count = Institution.objects.annotate(
        researcher_count=Count('researcherregistrations')
    ).filter(researcher_count__lte=20).aggregate(count=Count('id'))['count'] or 0

    # Combine institutions above 20 and count into a list for institutions
    by_institution = []
    for item in institutions_above_20:
        by_institution.append({
            'institution__name': item['name'],
            'researcher_count': item['researcher_count'],
        })
    
    # Add "Other Institutions" category with its count to the list for institutions
    by_institution.append({
        'institution__name': 'Other Institutions',
        'researcher_count': other_institutions_count,
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
