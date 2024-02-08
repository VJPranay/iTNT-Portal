from ..models import StudentRegistrations
from django.shortcuts import render
from django.http import JsonResponse
from datarepo.models import AreaOfInterest,State,Department,Institution,District
from django.http import JsonResponse
import string
from django.http import JsonResponse




def student_registration(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name',None)
        institution_id = request.POST.get('institution',None)
        department_id = request.POST.get('department',None)
        year_of_graduation = request.POST.get('year_of_graduation',None)
        district_id = request.POST.get('district',None)
        state_id = request.POST.get('state',None)
        project_idea = request.POST.get('project_idea',None)
        area_of_interest_ids = request.POST.get('area_of_interest',None)

        try:
            # Creating a new StudentRegistration object
            new_student_registration = StudentRegistrations.objects.create(
                name=name,
                institution_id=institution_id,
                department_id=department_id,
                year_of_graduation=year_of_graduation,
                district_id=district_id,
                state_id=state_id,
                project_idea=project_idea
            )

            # Adding multiple AreaOfInterest objects to the ManyToManyField
            new_student_registration.area_of_interest.add(*area_of_interest_ids)

            # Optionally, you can return a success response
            return JsonResponse({
                'success': True,
                'registration_id': str(new_student_registration.id),
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'registration_id': "Failed",
                'error': str(e),
            })

    elif request.method == 'GET':
        return render(request, 'registrations/industry_registration.html', context={
            'institutions': [
                {
                    'institution_id': x.id,
                    'institution_name': x.name
                }for x in Institution.objects.all()
            ],
            
            'departments':[
                {
                
                'department_id': x.id,
                'department_name': x.name
               }for x in Department.objects.all()
            ] ,
            
            'districts': [
                {
                    'district_id': x.id,
                    'district_name': x.name
                }for x in District.objects.all()
            ],
            
            'states': [
                {
                    'state_id': x.id,
                    'state_name': x.name
                }for x in State.objects.all()
            ],
            
            'area_of_interests': [
                {
                    'area_of_interest_id': x.id,
                    'area_of_interest_name': x.name
                }for x in AreaOfInterest.objects.all()
                ],
        })