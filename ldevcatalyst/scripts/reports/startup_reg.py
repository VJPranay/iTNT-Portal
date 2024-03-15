from registrations.models import StartUpRegistrations


from django.db.models import Count

startup_count_by_interest = StartUpRegistrations.objects.values('area_of_interest__name').annotate(startup_count=Count('id')).order_by('-startup_count')

# Access the results
for item in startup_count_by_interest:
    print(f"{item['area_of_interest__name']}: {item['startup_count']}")


startup_count_by_district = StartUpRegistrations.objects.values('district__name').annotate(startup_count=Count('id')).order_by('-startup_count')

# Access the results
for item in startup_count_by_district:
    print(f"{item['district__name']}: {item['startup_count']}")


startup_count_by_funding_stage = StartUpRegistrations.objects.values('funding_stage__name').annotate(startup_count=Count('id')).order_by('-startup_count')

# Access the results
for item in startup_count_by_funding_stage:
    print(f"{item['funding_stage__name']}: {item['startup_count']}")
