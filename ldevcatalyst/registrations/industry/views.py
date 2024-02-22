from django.shortcuts import render
from django.http import JsonResponse
from ..models import IndustryRegistrations
from datarepo.models import AreaOfInterest,State,IndustryCategory
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
import json
from profiles.models import Industry
from cerberus import Validator
import json
from django.utils.html import escape
import yaml



@login_required
def industry_registrations(request,registration_status=None):
    if registration_status is not None:
        industry_registrations = IndustryRegistrations.objects.filter(status=registration_status)
    else:
        industry_registrations = IndustryRegistrations.objects.all()
    industry_registrations_list = []
    for x in industry_registrations:
        temp = {
            'industry_id' : x.id,
            'name':x.name,
            'industry' : x.industry,
            'district' : x.district.name,
            'state':x.state.name,
            'mobile' : x.mobile,
            'created' : x.created,
        }
        industry_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/industry/list.html',context={'industry_registrations':industry_registrations_list})


@login_required
def industry_approve_registration(request):
    if request.method == 'POST':

        registration_id = request.POST.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = IndustryRegistrations.objects.get(id=registration_id)
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
                    return JsonResponse({'success': True},status=200)
                industry_profile=Industry.objects.create(
                    user_id=user.id,
                    name = registration.name,
                    industry = registration.industry,
                    state =  registration.state,
                    district = registration.district,
                    point_of_contact_name = registration.point_of_contact_name,
                    email = registration.email,
                    mobile = registration.mobile,
                    created = registration.created,
                    updated = registration.updated
                )
                industry_profile.save()
                for x in registration.area_of_interest.all():
                    industry_profile.area_of_interest.add(x.id)
                    industry_profile.save()
                    
                print(user.username)
                email_host = 'mail.ldev.in'
                email_port = 465
                email_username = 'itntadmin@ldev.in'
                email_password = 'Pranay123@'
                subject = 'You iTNT registration has been approved'
                body = f'''
                        Username: {user.username}
                        Password: {password}
                        Login URL: http://innovationportal.tnthub.org.ldev.in/dashboard
                        '''
                print(password)
                message = MIMEMultipart()
                message['From'] = email_username
                message['To'] = registration.email  # Add the additional email address
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                with smtplib.SMTP_SSL(email_host, email_port) as server:
                    print(server.login(email_username, email_password))
                    print(server.sendmail(email_username, [registration.email], message.as_string()))
                return JsonResponse({'success': True})
            except IndustryRegistrations.DoesNotExist:
                print("error")
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
        area_of_interest_id = request.POST.getlist('collaboration_sector')
        request_schema ='''
        company_name:
            type: string
            required: true
            minlength: 5
            
        csrfmiddlewaretoken:
            type: string
            required: true
            minlength: 5

        industry_type:
            type: string
            required: true

        location_state:
            type: string
            required: true

        location_district:
            type: string
            required: true

        poc_name:
            type: string
            required: true
            minlength: 5


        poc_email:
            type: string
            required: true
            regex: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'


        poc_mobile:
            type: string
            required: true
            regex: '^\d{10}$'


        collaboration_sector:
            type: string
            required: true

        '''
        v=Validator()
        post_data = request.POST.dict()
        schema=yaml.load(request_schema, Loader=yaml.SafeLoader)
        if v.validate(post_data,schema):
            print(post_data)
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
        else:
            return JsonResponse(
                    {
                        'success': False,
                        'registration_id': "Failed",
                        'error': v.errors,
                    })
    elif request.method == 'GET':
        return render(request,'registrations/industry_registration.html',context={ 
                         
        'industry_types' : [
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
    


@login_required
def fetch_industry_registration_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        industry_id = data.get('industry_id',None)
        if not industry_id:
            return JsonResponse({'error': 'Invalid industry ID'}, status=400)
        # Fetch industry details based on industry_id
        print(industry_id)
        industry = IndustryRegistrations.objects.get(id=industry_id)
        area_of_interest_html = ""
        for interest in industry.area_of_interest.all():
            area_of_interest_html += f"{interest.name}"
        # Construct HTML for the industry details
        html = f"""
                
                                            <!--begin::Profile-->
                                            <div class="d-flex gap-7 align-items-center">
                                                <!--begin::Avatar-->
                                                <div class="symbol symbol-circle symbol-100px">
                                                    <span class="symbol-label bg-light-success fs-1 fw-bolder">"""+escape(industry.name[:1])+"""</span>
                                                </div>
                                                <!--end::Avatar-->
                                                <!--begin::Contact details-->
                                                <div class="d-flex flex-column gap-2">
                                                    <!--begin::Name-->
                                                    <h3 class="mb-0">"""+escape(industry.name)+"""</h3>
                                                    <!--end::Name-->
                            
                                                    <!--begin::Phone-->
                                                    <div class="d-flex align-items-center gap-2">
                                                        <i class="ki-outline ki-phone fs-2"></i>
                                                        <a href="#" class="text-muted text-hover-primary">"""+escape(industry.mobile)+"""</a>
                                                    </div>
                                                    <!--end::Phone-->
                                                </div>
                                                <!--end::Contact details-->
                                            </div>
                                            <!--end::Profile-->
                                            <!--begin:::Tabs-->
                                            <ul class="nav nav-custom nav-tabs nav-line-tabs nav-line-tabs-2x fs-6 fw-semibold mt-6 mb-8 gap-2">
                                                <!--begin:::Tab item-->
                                                <li class="nav-item">
                                                    <a class="nav-link text-active-primary d-flex align-items-center pb-4 active" data-bs-toggle="tab" href="#kt_contact_view_general">
                                                    <i class="ki-outline ki-home fs-4 me-1"></i>Information</a>
                                                </li>
                                                <!--end:::Tab item-->
                                            </ul>
                                            <!--end:::Tabs-->
                                            <!--begin::Tab content-->
                                            <div class="tab-content" id="">
                                                <!--begin:::Tab pane-->
                                                <div class="tab-pane fade show active" id="kt_contact_view_general" role="tabpanel">
                                                    <!--begin::Additional details-->
                                                    <div class="d-flex flex-column gap-5 mt-7">
                                                        <!--begin::state-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">State</div>
                                                            <div class="fw-bold fs-5">"""+escape(industry.state.name)+"""</div>
                                                        </div>
                                                        <!--end::state-->
                                                        <!--begin::district-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">District</div>
                                                            <div class="fw-bold fs-5">"""+escape(industry.district.name)+"""</div>
                                                        </div>
                                                        <!--end::district-->
                                                       
                                                        <!--end::end year_of_graduation-->
                                                        <!--begin::point_of_contact_name-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">point of contact name</div>
                                                            <div class="fw-bold fs-5">"""+escape(industry.point_of_contact_name)+"""</div>
                                                        </div>
                                                        <!--end::point_of_contact_name-->
                                                         <!--begin::email-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">Email</div>
                                                            <div class="fw-bold fs-5">"""+escape(industry.email)+"""</div>
                                                        </div>
                                                        <!--end::email-->
                                                        
                                                        <!--begin::industry-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">Industry</div>
                                                            <div class="fw-bold fs-5">"""+escape(industry.name)+"""</div>
                                                        </div>
                                                        <!--end::indusrty-->
                                                        <!--begin::area_of_interest-->
                                                        <div class="d-flex flex-column gap-1">
                                                            <div class="fw-bold text-muted">Area of Interest</div>
                                                            <div class="fw-bold fs-5">""" +escape(area_of_interest_html)+"""</div>
                                                        </div>
                                                        <!--end::area_of_interest-->
                                                        
                                                    </div>
                                                    <!--end::Additional details-->
                                                </div>
                                                <!--end:::Tab pane-->
                                            </div>
                                            <!--end::Tab content-->
                        """
        return JsonResponse({'html': html})
    else:
        # Handle invalid request
        return JsonResponse({'error': 'Invalid request'}, status=400)