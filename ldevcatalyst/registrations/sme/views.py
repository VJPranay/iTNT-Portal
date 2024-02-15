from django.shortcuts import render
from django.http import JsonResponse
from ..models import ResearcherRegistrations
from datarepo.models import AreaOfInterest,State
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
def sme_registrations(request,registration_status=None):
    if registration_status is not None:
        sme_registrations = ResearcherRegistrations.objects.filter(status=registration_status)
    else:
        sme_registrations = ResearcherRegistrations.objects.all()
    sme_registrations_list = []
    for x in sme_registrations:
        temp = {
            'id' : x.id,
            'company' : x.name,
            'sme' : x.sme.name,
            'district' : x.district.name,
            'mobile' : x.mobile,
            'created' : x.created,
        }
        sme_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/sme/list.html',context={'sme_registrations':sme_registrations_list})


@login_required
def sme_approve_registration(request):
    if request.method == 'POST':

        registration_id = request.POST.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = ResearcherRegistrations.objects.get(id=registration_id)
                registration.status = 'approved'
                registration.save()
                
                # Generate username from registration ID
                username = registration.registration_id
                print(username)

                # Generate random 6-digit number
                password = ''.join(random.choices(string.digits, k=6))
                print(password)

                # Create user with the generated username and random password
                try:
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.user_role = 4
                    user.email = registration.email
                    user.save()
                except IntegrityError:
                    user = User.objects.get(username=username)
                    user.delete()
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.user_role = 4
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
            except ResearcherRegistrations.DoesNotExist:
                print("error")
                return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def sme_registration(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('company_name')
        sme_id = request.POST.get('sme_type')
        state_id = request.POST.get('location_state')
        district_id = request.POST.get('location_district')
        poc_name = request.POST.get('poc_name')
        poc_email = request.POST.get('poc_email')
        poc_mobile = request.POST.get('poc_mobile')
        area_of_interest_id = request.POST.get('collaboration_sector')
        try:
            new_sme_registration = ResearcherRegistrations.objects.create(
                name = name,
                sme_id = sme_id,
                state_id = state_id,
                district_id = district_id,
                point_of_contact_name = poc_name,
                email = poc_email,
                mobile = poc_mobile,
            )
            new_sme_registration.save()
            new_sme_registration.area_of_interest.add(area_of_interest_id)
            new_sme_registration.save()
            # Optionally, you can return a success response
            return JsonResponse(
                {
                    'success': True,
                    'registration_id': str(new_sme_registration.registration_id),
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
        return render(request,'registrations/sme_registration.html',context={ 
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