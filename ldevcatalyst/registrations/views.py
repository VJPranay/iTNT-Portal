from django.shortcuts import render
from django.http import JsonResponse
from .models import IndustryRegistrations
# Create your views here.
def industry_registrations(request):
    return render(request, 'dashboard/registrations/industry/list.html')


def industry_registration(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('company_name')
        industry_id = request.POST.get('industry_type')
        state_id = request.POST.get('location_state')
        district_id = request.POST.get('location_district')
        poc_name = request.POST.get('poc_name')
        poc_email = request.POST.get('poc_email')
        poc_mobile = request.POST.get('poc_mobile')
        area_of_interest_id = request.POST.get('collaboration_sector')
        try:
            new_industry_registration = IndustryRegistrations.objects.create(
                name = name,
                industry_id = industry_id,
                state_id = state_id,
                district_id = district_id,
                point_of_contact_name = poc_name,
                email = poc_email,
                mobile = poc_mobile,
            )
            new_industry_registration.save()
            new_industry_registration.area_of_interest.add(area_of_interest_id)
            new_industry_registration.save()
            # Optionally, you can return a success response
            return JsonResponse(
                {
                    'success': True,
                    'registration_id': str(new_industry_registration.id),
                }
                )
        except Exception as e:
            return JsonResponse(
                {
                    'success': False,
                    'registration_id': "Failed",
                    'error': str(e),
                }
                )
    elif request.method == 'GET':
        return render(request,'registrations/industry_registration.html')