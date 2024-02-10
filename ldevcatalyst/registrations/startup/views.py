from django.shortcuts import render
from django.http import JsonResponse
from ..models import StartUpRegistrations
from datarepo.models import AreaOfInterest,State,PreferredInvestmentStage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
import string
from django.http import JsonResponse
from profiles.models import User
from django.db.utils import IntegrityError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart



@login_required
def startup_registrations(request,registration_status=None):
    if registration_status is not None:
        startup_registrations = StartUpRegistrations.objects.filter(status=registration_status)
    else:
        startup_registrations = StartUpRegistrations.objects.all()
    startup_registrations_list = []
    for x in startup_registrations:
        temp = {
            'id' : x.id,
            'name' : x.name,
            'area_of_interest' : x.area_of_interest.name,
            'district' : x.district.name,
            'funding_stage' : x.funding_stage.name,
            'mobile' : x.mobile,
            'created' : x.created,
        }
        startup_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/startup/list.html',context={'startup_registrations':startup_registrations_list})


@login_required
def startup_approve_registration(request):
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = StartUpRegistrations.objects.get(id=registration_id)
                registration.status = 'approved'
                registration.save()
                
                # Generate username from registration ID
                username = registration.registration_id

                # Generate random 6-digit number
                password = ''.join(random.choices(string.digits, k=6))

                # Create user with the generated username and random password
                try:
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.user_role = 6
                    user.email = registration.email
                    user.save()
                except IntegrityError:
                    user = User.objects.get(username=username)
                    user.delete()
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.user_role = 6
                    user.email = registration.email
                    user.save()
                print(user.username)
                email_host = 'mail.ldev.in'
                email_port = 465
                email_username = 'itntadmin@ldev.in'
                email_password = 'Pranay123@'
                subject = 'You iTNT registration has been approved'
                body = f'''
                        Username: {user.username}
                        Password: {password}
                        Login URL: https://ldev.in
                        '''
                message = MIMEMultipart()
                message['From'] = email_username
                message['To'] = registration.email  # Add the additional email address
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                with smtplib.SMTP_SSL(email_host, email_port) as server:
                    print(server.login(email_username, email_password))
                    print(server.sendmail(email_username, [registration.email], message.as_string()))
                return JsonResponse({'success': True})
            except StartUpRegistrations.DoesNotExist:
                print("error")
                return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def startup_registration(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        print(request.POST)
        name = request.POST.get('name')
        co_founder_count = request.POST.get('co_founder_count')
        founder_names = request.POST.get('founder_names')
        district_id = request.POST.get('location_district')
        state_id = request.POST.get('location_state')
        area_of_interest_id = request.POST.get('area_of_interest_id')
        funding_stage_id = request.POST.get('funding_stage_id')
        team_size = request.POST.get('team_size')
        email = request.POST.get('poc_email')
        mobile = request.POST.get('poc_mobile')
        dpiit_number = request.POST.get('dpiit_number')
        
        description = request.POST.get('description')
        
        pitch_deck = request.POST.get('pitch_deck')
        video_link = request.POST.get('video_link')
        website = request.POST.get('company_website')
        try:
            new_startup_registration = StartUpRegistrations.objects.create(
                name = name,
                co_founder_count = co_founder_count,
                founder_names = founder_names,
                district_id = district_id,
                state_id = state_id,
                team_size = team_size,
                email = email,
                mobile = mobile,
                dpiit_number = dpiit_number,
                area_of_interest_id = area_of_interest_id,
                description = description,
                funding_stage_id = funding_stage_id,
                pitch_deck = pitch_deck,
                video_link = video_link,
                website = website,
            )
            new_startup_registration.save()
            # Optionally, you can return a success response
            return JsonResponse(
                {
                    'success': True,
                    'registration_id': str(new_startup_registration.registration_id),
                }
                )
        except Exception as e:
            print(e)
            return JsonResponse(
                {
                    'success': False,
                    'registration_id': "Failed",
                    'error': str(e),
                }
                )
    elif request.method == 'GET':
        return render(request,'registrations/startup_registration.html',context={ 
                         
        'preferred_investment_stages' : [
            {
                'preferred_investment_stage_id' : x.id,
                'preferred_investment_stage_value' : x.name,
            } for x in PreferredInvestmentStage.objects.all()
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