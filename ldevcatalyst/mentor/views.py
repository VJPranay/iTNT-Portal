from django.shortcuts import render
from .models import MentorRegistration
import random
import yaml
from cerberus import Validator
import json
import string
from profiles.models import User,Mentor
from django.utils.html import escape
from django.db.utils import IntegrityError
from django.http import JsonResponse
from ldevcatalyst import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from datarepo.models import AreaOfInterest,State,District
from django.shortcuts import get_object_or_404

# Create your views here.

def mentor_registrations(request,registration_status=None):
    if registration_status is not None:
        mentor_registrations = MentorRegistration.objects.filter(status=registration_status)
    else:
        mentor_registrations = MentorRegistration.objects.all()
    mentor_registrations_list = []
    for x in mentor_registrations:
        temp = {
            'mentor_id' : x.id,
            'name':x.name,
            'area_of_interest' : x.area_of_interest.area_of_interest_value,
            'mobile' : x.mobile,
            'created' : x.created,
        }
        mentor_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/mentor/list.html',context={'mentor_registrations':mentor_registrations_list})



def mentor_approve_registration(request):
    if request.method == 'POST':

        registration_id = request.POST.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = MentorRegistration.objects.get(id=registration_id)
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
                    user.user_role = 9
                    user.email = registration.email
                    user.save()
                except IntegrityError:
                   user = User.objects.get(username=username)
                   return JsonResponse({'success': True},status=200)
                mentor_profile=Mentor.objects.create(
                    user_id=user.id,
                    name=registration.name,
                    mobile=registration.mobile,
                    email=registration.email,
                    address=registration.address,
                    linkedin_url=registration.linkedin_url,
                    company_name=registration.company_name,
                    designation=registration.designation,
                    profile_picture=registration.profile_picture,
                    updated_bio=registration.updated_bio,
                    certified_mentor=registration.certified_mentor,
                    reason=registration.reason,
                    area_of_interest=registration.area_of_interest,
                    functional_areas_of_expertise=registration.functional_areas_of_expertise,
                    mentoring_experience=registration.mentoring_experience,
                    motivation_for_mentoring=registration.motivation_for_mentoring,
                    category_represent_you=registration.category_represent_you,
                    mentees_journey=registration.mentees_journey,
                    gender=registration.gender,
                    state_id=registration.state_id,
                    district_id=registration.district_id,
                    commitment_as_mentor=registration.commitment_as_mentor,
                    intensive_mentoring_program=registration.intensive_mentoring_program,
                    approved=True

                )
                mentor_profile.save()
                
                print(user.username)
                email_host = settings.email_host
                email_port = settings.email_port
                email_username = settings.email_username
                email_password = settings.email_password
                email_from = settings.email_from
                subject = 'You iTNT registration has been approved'
                body = f'''
                        Username: {user.username}
                        Password: {password}
                        Login URL: https://itnthub.tn.gov.in/innovation-portal/dashboard
                        '''
                print(password)
                message = MIMEMultipart()
                message['From'] = 'aso.itnt@tn.gov.in'
                message['To'] = registration.email  # Add the additional email address
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                with smtplib.SMTP_SSL(email_host, email_port) as server:
                    server.login(email_username, email_password)
                    server.sendmail(email_from, [registration.email], message.as_string())
                return JsonResponse({'success': True})
            except MentorRegistration.DoesNotExist:
                print("error")
                return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)




def mentor_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        mobile = request.POST.get('mobile')
        email = request.POST.get('email')
        address = request.POST.get('address')
        linkedin_url = request.POST.get('linkedin_url')
        company_name = request.POST.get('company_name')
        designation = request.POST.get('designation')
        profile_picture = request.FILES.get('profile_picture')
        updated_bio = request.FILES.get('updated_bio')
        certified_mentor = request.POST.get('certified_mentor')=='yes'
        reason=request.POST.get('reason','')
        area_of_interest_id = request.POST.get('collaboration_sector')
        functional_areas_of_expertise = request.POST.get('functional_areas_of_expertise')
        mentoring_experience = request.POST.get('mentoring_experience')
        motivation_for_mentoring = request.POST.get('motivation_for_mentoring')
        category_represent_you = request.POST.get('category_represent_you')
        mentees_journey = request.POST.get('mentees_journey')
        commitment_as_mentor=request.POST.get('commitment_as_mentor')
        intensive_mentoring_program=request.POST.get('intensive_mentoring_program')
        state_id=request.POST.get('state_id')
        district_id=request.POST.get('district_id')
        gender = request.POST.get('gender')
        
        # Convert certified_mentor_str to Boolean
        #certified_mentor = certified_mentor.lower() == 'yes'
        intensive_mentoring_program = intensive_mentoring_program.lower() == 'yes'
        
        request_schema = '''
        name:
            type: string
            required: true
            minlength: 5
            
        csrfmiddlewaretoken:
            type: string
            required: true
            minlength: 5
            
        mobile:
            type: string
            required: true
            regex: '^\d{10}$'

        email:
            type: string
            required: true
            regex: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'

        address:
            type: string
            required: true
            
        linkedin_url:
            type: string
            required: false

        company_name:
            type: string
            required: true
        designation:
            type: string
            required: true
            
        certified_mentor:
            type: string
            required: true
        
        collaboration_sector:
            type: string
            required: true  
        
            
        functional_areas_of_expertise:
            type: string
            required: true
            
        mentoring_experience:
            type: string
            required: true
            
        motivation_for_mentoring:
            type: string
            required: true
            
        category_represent_you:
            type: string
            required: true
            
        mentees_journey:
            type: string
            required: true
            
        gender:
            type: string
            required: true
            
        district_id:
            type: string
            required: true
        state_id:
            type: string
            required: true
            
        commitment_as_mentor:
            type: string
            required: true
            
        intensive_mentoring_program:
            type: string
            required: true
        
        reason:
            type: string
            required: true
            
        '''
        
        v = Validator()
        post_data = request.POST.dict()
        schema = yaml.load(request_schema, Loader=yaml.SafeLoader)
        
        if v.validate(post_data, schema):
            try:
                area_of_interest = get_object_or_404(AreaOfInterest, id=area_of_interest_id)
                
                new_mentor_registration = MentorRegistration.objects.create(
                    name=name,
                    mobile=mobile,
                    email=email,
                    address=address,
                    linkedin_url=linkedin_url,
                    company_name=company_name,
                    designation=designation,
                    profile_picture=profile_picture,
                    updated_bio=updated_bio,
                    certified_mentor=certified_mentor,
                    reason=reason,
                    area_of_interest=area_of_interest,
                    functional_areas_of_expertise=functional_areas_of_expertise,
                    mentoring_experience=mentoring_experience,
                    motivation_for_mentoring=motivation_for_mentoring,
                    category_represent_you=category_represent_you,
                    mentees_journey=mentees_journey,
                    gender=gender,
                    state_id=state_id,
                    district_id=district_id,
                    commitment_as_mentor=commitment_as_mentor,
                    intensive_mentoring_program=intensive_mentoring_program
                )
                new_mentor_registration.save()
                return JsonResponse(
                    {
                        'success': True,
                        'registration_id': str(new_mentor_registration.registration_id),
                    }
                    )
            except IntegrityError as e:
                return JsonResponse({'success': False, 'registration_id': "Failed", 'error': str(e)})
        else:
            return JsonResponse({'success': False, 'registration_id': "Failed", 'error': v.errors})
    
    elif request.method == 'GET':
        return render(request, 'registrations/mentor_registration.html', context={
            'area_of_interests': [
                {
                    'area_of_interest': x.id,
                    'area_of_interest_value': x.name,
                } for x in AreaOfInterest.objects.filter(is_approved=True)
            ],
            'states' : [
                {
                    'state_id' : x.id,
                    'state_value' : x.name,
                } for x in State.objects.all().order_by('name')
            ],
            'districts' : [
                {
                    'district_id' : x.id,
                    'district_value' : x.name,
                } for x in District.objects.all().order_by('name')
            ]
        })
