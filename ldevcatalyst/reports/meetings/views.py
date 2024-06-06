from django.db.models import Count
from django.http import JsonResponse
from django.shortcuts import render
from meetings.models import MeetingRequests

# def meeting_counts(request):
#     # Query to get meeting counts by VC
#     meeting_counts_vc = MeetingRequests.objects.values('vc__firm_name').annotate(total_meetings=Count('id')).order_by('-total_meetings')

#     # Query to get meeting counts by Next Level
#     meeting_counts_next_level = MeetingRequests.objects.values('next_level').annotate(total_meetings=Count('id')).order_by('-total_meetings')
#     startups_next_level = MeetingRequests.objects.filter(next_level=True).select_related('start_up', 'vc').order_by('start_up__name')

#     # Increment index for displaying serial number in template
#     for index, item in enumerate(startups_next_level):
#         item.index = index + 1

#     context = {
#         'meeting_counts_vc': meeting_counts_vc,
#         'meeting_counts_next_level': meeting_counts_next_level,
#         'startups_next_level': startups_next_level,
#     }

#     return render(request, 'dashboard/reports/meetings/overview.html', context)

def meeting_counts(request):
    # Query to get meeting counts by VC
    meeting_counts_vc = MeetingRequests.objects.values('vc__firm_name').annotate(total_meetings=Count('id')).order_by('-total_meetings')

    # Query to get meeting counts by Next Level
    meeting_counts_next_level = MeetingRequests.objects.values('next_level').annotate(total_meetings=Count('id')).order_by('-total_meetings')
    startups_next_level = MeetingRequests.objects.filter(next_level=True).select_related('start_up', 'vc').order_by('start_up__company_name')  # Use 'company_name' instead of 'name'

    # Increment index for displaying serial number in template
    for index, item in enumerate(startups_next_level):
        item.index = index + 1

    context = {
        'meeting_counts_vc': meeting_counts_vc,
        'meeting_counts_next_level': meeting_counts_next_level,
        'startups_next_level': startups_next_level,
    }

    return render(request, 'dashboard/reports/meetings/overview.html', context)