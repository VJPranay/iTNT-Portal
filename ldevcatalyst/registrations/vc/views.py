from django.shortcuts import render
from django.http import JsonResponse
from ..models import VCRegistrations
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
def vc_registrations(request,registraion_status=None):
    if registraion_status is not None:
        vc_registrations = VCRegistrations.objects.filter(status=registraion_status)
    else:
        vc_registrations = VCRegistrations.objects.all()
    vc_registrations_list = []
    for x in vc_registrations:
        temp = {
            'id' : x.id,
            'firm_name' : x.firm_name,
            'partner_name' : x.partner_name,
            'district' : x.district.name,
            'mobile' : x.mobile,
            'created' : x.created,
        }
        vc_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/vc/list.html',context={'vc_registrations':vc_registrations_list})


@login_required
def vc_approve_registration(request):
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id',None)

        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = VCRegistrations.objects.get(id=registration_id)
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
                    user.save()
                except IntegrityError:
                    user = User.objects.get(username=username)
                    user.delete()
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
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
            except VCRegistrations.DoesNotExist:
                print("error")
                return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def vc_registration(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        print(request.POST)
        partner_name = request.POST.get('partner_name')
        firm_name = request.POST.get('firm_name')
        email = request.POST.get('poc_email')
        mobile = request.POST.get('poc_mobile')
        district_id = request.POST.get('location_district')
        state_id = request.POST.get('location_state')
        area_of_interest_id = request.POST.get('collaboration_sector')
        funding_stage_id = request.POST.get('funding_stage_id')
        company_website = request.POST.get('company_website')
        linkedin_profile = request.POST.get('linkedin_profile')
        try:
            new_vc_registration = VCRegistrations.objects.create(
                partner_name = partner_name,
                firm_name = firm_name,
                email = email,
                mobile = mobile,
                district_id = district_id,
                state_id = state_id,
                funding_stage_id = funding_stage_id,
                area_of_interest_id = area_of_interest_id,
                company_website = company_website,
                linkedin_profile = linkedin_profile,
            )
            new_vc_registration.save()
            # Optionally, you can return a success response
            return JsonResponse(
                {
                    'success': True,
                    'registration_id': str(new_vc_registration.registration_id),
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
        return render(request,'registrations/vc_registration.html',context={ 
                         
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