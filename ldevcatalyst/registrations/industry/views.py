from django.shortcuts import render
from django.http import JsonResponse
from ..models import IndustryRegistrations
from datarepo.models import AreaOfInterest,State,IndustryCategory
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse




@login_required
def industry_registrations(request,registraion_status=None):
    if registraion_status is not None:
        industry_registrations = IndustryRegistrations.objects.filter(status=registraion_status)
    else:
        industry_registrations = IndustryRegistrations.objects.all()
    industry_registrations_list = []
    for x in industry_registrations:
        temp = {
            'id' : x.id,
            'company' : x.name,
            'industry' : x.industry.name,
            'district' : x.district.name,
            'mobile' : x.mobile,
            'created' : x.created,
        }
        industry_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/industry/list.html',context={'industry_registrations':industry_registrations_list})


@login_required
def approve_registration(request):
    if request.method == 'POST':
        print(request.POST)
        registration_id = request.POST.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = IndustryRegistrations.objects.get(id=registration_id)
                registration.status = 'approved'
                registration.save()
                return JsonResponse({'success': True})
            except IndustryRegistrations.DoesNotExist:
                return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


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
                    'registration_id': str(new_industry_registration.registration_id),
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
        return render(request,'registrations/industry_registration.html',context={ 
                         
        'indsutry_types' : [
            {
                'industry_id' : x.id,
                'industry_value' : x.name,
            } for x in IndustryCategory.objects.all()
        ],
        'states' : [
            {
                'state_id' : x.id,
                'state_value' : x.name,
            } for x in State.objects.all()
        ],
        'area_of_interests' : [
            {
                'area_of_interest_id' : x.id,
                'area_of_interest_value' : x.name,
            } for x in AreaOfInterest.objects.all()    
        ]})