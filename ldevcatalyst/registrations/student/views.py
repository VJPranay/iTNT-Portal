from ..models import StudentRegistrations
from django.shortcuts import render
from django.http import JsonResponse
from datarepo.models import AreaOfInterest,State,Department,Institution,District
from django.http import JsonResponse
import string
from django.contrib.auth.decorators import login_required
from profiles.models import User
from django.db.utils import IntegrityError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


@login_required
def approve_student_registrations(request):
    if request.method=='POST':
        registration_id=request.post.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success':False,'error':'Missing registration ID'},status=400)
        else:
            try:
                registration=StudentRegistrations.objects.get(id=registration_id)
                registration.status='approved'
                registration.save()
                
                #Generate Userneme from Registaration Id
                username=registration.registration_id
                print(username)
                
                #Generating Randon 6 digit number
                password=" ".join(random.choices(string.digits,k=6))
                print(password)
                
                #Create User with Username and random Password
                try:
                    user=User.objects.create_user(username=username,password=password)
                    user.is_active=True
                    user.save()
                except IntegrityError :
                    user=User.objects.get(username=username)
                    user.delete()
                    user=User.objects.create(usename=username,password=password)
                    user.is_active=True
                    user.save()
                print(user.username)
                email_host='mail.ldev.in'
                email_port = 465
                email_username = 'itntadmin@ldev.in'
                email_password = 'Pranay123@'
                subject = 'You iTNT registration has been approved'
                body = f'''
                        Username: {user.username}
                        Password: {password}
                        Login URL: https://ldev.in
                        '''
                message=MIMEMultipart()
                message['From']=email_username
                message['To']=registration.email
                message['Subject']=subject
                message.attach(MIMEText(body,'plain'))
                with smtplib.SMTP_SSL(email_host,email_port) as server:
                    print(server.login(email_username,email_password))   
                    print(server.sendmail(email_username,[registration.email],message.as_string()))  
                return JsonResponse({'success':True}) 
            except  StudentRegistrations.DoesNotExist:
                print('error')
                return JsonResponse({'status':False,'error':'Registration not found'},status=404)
    else:
        return JsonResponse({'status':False,'error':'Method not allowed'},status=405)
                 
                
                
        
def student_registration(request):
    if request.method == 'POST':
        try:
            # Retrieve data from the POST request
            name = request.POST.get('name')
            institution_id = request.POST.get('institution_id')
            department_id = request.POST.get('department_id')
            year_of_graduation = request.POST.get('year_of_graduation')
            district_id = request.POST.get('location_district')
            state_id = request.POST.get('location_state')
            project_idea = request.POST.get('project_idea')
            area_of_interest_ids = request.POST.getlist('area_of_interest')
            
            # Perform validation on the received data (e.g., ensure required fields are not empty)
            if not (name and institution_id and department_id and year_of_graduation and district_id and state_id and project_idea and area_of_interest_ids):
                raise ValueError("Missing required fields")

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
            new_student_registration.save()
                        
            
            # Return a success response
            return JsonResponse({
                'success': True,
                'registration_id': str(new_student_registration.registration_id),
            })
        except IntegrityError as e:
            return JsonResponse({
                'success': False,
                'registration_id': "Failed",
                'error': "IntegrityError: " + str(e),
            })
        except ValueError as e:
            return JsonResponse({
                'success': False,
                'registration_id': "Failed",
                'error': str(e),
            })
        except Exception as e:
            return JsonResponse({
                'success': False,
                'registration_id': "Failed",
                'error': "An error occurred: " + str(e),
            })

    elif request.method == 'GET':
        # Return the initial form data
        return render(request, 'registrations/student_registration.html', context={
            'institutions': [
                {'institution_id': x.id, 'institution_name': x.name} for x in Institution.objects.all()
            ],
            'departments': [
                {'department_id': x.id, 'department_name': x.name} for x in Department.objects.all()
            ],
            'districts': [
                {'district_id': x.id, 'district_name': x.name} for x in District.objects.all()
            ],
            'states': [
                {'state_id': x.id, 'state_name': x.name} for x in State.objects.all()
            ],
            'area_of_interests': [
                {'area_of_interest_id': x.id, 'area_of_interest_name': x.name} for x in AreaOfInterest.objects.all()
            ],
        })