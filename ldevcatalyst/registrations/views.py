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
        print("name", name)
        print("industry_id", industry_id)
        print("state_id", state_id)
        print("district_id", district_id)
        print("poc_name", poc_name)
        print("poc_email", poc_email)
        print("poc_mobile", poc_mobile)
        print("area_of_interest_id", area_of_interest_id)
        # Optionally, you can return a success response
        return JsonResponse(
            {
                'success': True,
                'registration_id': "123123HHHHSDDD",
             }
            )
    elif request.method == 'GET':
        return render(request,'registrations/industry_registration.html')