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
from datarepo.models import AreaOfInterest

from django.shortcuts import get_object_or_404

# Create your views here.

def mentor_registrations(request,registration_status=None):
    if registration_status is not None:
        mentor_registrations = MentorRegistration.objects.filter(status=registration_status)
    else:
        mentor_registrations = MentorRegistration.objects.all()
    student_registrations_list = []
    for x in mentor_registrations:
        temp = {
            'mentor_id' : x.id,
            'name':x.name,
            'area_of_interest' : x.area_of_interest.area_of_interest_value,
            'mobile' : x.mobile,
            
           
            
            'created' : x.created,
        }
        student_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/student/list.html',context={'student_registrations':student_registrations_list})



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
                    user.user_role = 7
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
                    area_of_interest=registration.area_of_interest,
                    functional_areas_of_expertise=registration.functional_areas_of_expertise,
                    mentoring_experience=registration.mentoring_experience,
                    motivation_for_mentoring=registration.motivation_for_mentoring,
                    category_represent_you=registration.category_represent_you,
                    mentees_journey=registration.mentees_journey,
                    gender=registration.gender,
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
        certified_mentor_str = request.POST.get('certified_mentor')
        area_of_interest_id = request.POST.get('collaboration_sector')
        functional_areas_of_expertise = request.POST.get('functional_areas_of_expertise')
        mentoring_experience = request.POST.get('mentoring_experience')
        motivation_for_mentoring = request.POST.get('motivation_for_mentoring')
        category_represent_you = request.POST.get('category_represent_you')
        mentees_journey = request.POST.get('mentees_journey')
        gender = request.POST.get('gender')
        
        # Convert certified_mentor_str to Boolean
        certified_mentor = certified_mentor_str.lower() == 'yes'
        
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
                    area_of_interest=area_of_interest,
                    functional_areas_of_expertise=functional_areas_of_expertise,
                    mentoring_experience=mentoring_experience,
                    motivation_for_mentoring=motivation_for_mentoring,
                    category_represent_you=category_represent_you,
                    mentees_journey=mentees_journey,
                    gender=gender
                )
                new_mentor_registration.save()
                
                registration = MentorRegistration.objects.get(id=new_mentor_registration.id)
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
                    user.user_role = 9
                    user.email = registration.email
                    user.save()
                except IntegrityError:
                    user = User.objects.get(username=username)
                    return JsonResponse({'success': True}, status=200)
                
                mentor_profile = Mentor.objects.create(
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
                    area_of_interest=registration.area_of_interest,
                    functional_areas_of_expertise=registration.functional_areas_of_expertise,
                    mentoring_experience=registration.mentoring_experience,
                    motivation_for_mentoring=registration.motivation_for_mentoring,
                    category_represent_you=registration.category_represent_you,
                    mentees_journey=registration.mentees_journey,
                    gender=registration.gender,
                    approved=True
                )
                mentor_profile.save()
                
                email_host = settings.EMAIL_HOST
                email_port = settings.email_port
                email_username = settings.EMAIL_HOST_USER
                email_password = settings.EMAIL_HOST_PASSWORD
                email_from = settings.email_from
                subject = 'Your iTNT registration has been approved'
                body = f'''
                Username: {user.username}
                Password: {password}
                Login URL: https://itnthub.tn.gov.in/innovation-portal/dashboard
                '''
                
                message = MIMEMultipart()
                message['From'] = email_from
                message['To'] = registration.email
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                
                with smtplib.SMTP_SSL(email_host, email_port) as server:
                    server.login(email_username, email_password)
                    server.sendmail(email_from, [registration.email], message.as_string())
                
                return JsonResponse({'success': True, 'registration_id': str(new_mentor_registration.registration_id)})
            
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
        })