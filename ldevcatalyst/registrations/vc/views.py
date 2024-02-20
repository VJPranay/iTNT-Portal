from django.shortcuts import render
from django.http import JsonResponse
from ..models import VCRegistrations
from datarepo.models import AreaOfInterest,State,PreferredInvestmentStage
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
import string
from django.http import JsonResponse
from profiles.models import User,VC
from django.db.utils import IntegrityError
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import json
import yaml
from cerberus import Validator
from django.db import IntegrityError





@login_required
def vc_registrations(request,registration_status=None):
    if request.user.user_role == 2:
        if registration_status is not None:
            vc_registrations = VCRegistrations.objects.filter(status=registration_status)
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
    else:
        return render(request, 'common/not_found.html')


@login_required
def vc_approve_registration(request):
    if request.user.user_role == 2:
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
                        user.user_role = 8
                        user.email = registration.email
                        user.save()
                    except IntegrityError:
                        user = User.objects.get(username=username)
                        return JsonResponse({'success': True})
                    # vc profile creation
                    vc_profile = VC.objects.create(
                        user_id = user.id,
                        partner_name = registration.partner_name,
                        firm_name = registration.firm_name,
                        email = registration.email,
                        mobile = registration.mobile,
                        deal_size_range_min = registration.deal_size_range_min,
                        deal_size_range_max = registration.deal_size_range_max,
                        portfolio_size = registration.portfolio_size,
                        district_id = registration.district.id,
                        state_id = registration.state.id,
                        area_of_interest_id = registration.area_of_interest.id,
                        funding_stage_id = registration.funding_stage.id,
                        company_website = registration.company_website,
                        linkedin_profile = registration.linkedin_profile,
                    )
                    vc_profile.save()
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
    else:
        return render(request, 'common/not_found.html')


def vc_registration(request):
    if request.method == 'POST':
        partner_name = request.POST.get('partner_name')
        firm_name = request.POST.get('firm_name')
        email = request.POST.get('poc_email')
        mobile = request.POST.get('poc_mobile')
        district_id = request.POST.get('location_district')
        state_id = request.POST.get('location_state')
        area_of_interest_id = request.POST.get('collaboration_sector')
        funding_stage_id = request.POST.get('funding_stage_id')
        deal_size_range_min = request.POST.get('deal_size_range_min')
        deal_size_range_max = request.POST.get('deal_size_range_max')
        portfolio_size = request.POST.get('portfolio_size')
        company_website = request.POST.get('company_website')
        linkedin_profile = request.POST.get('linkedin_profile')
        request_schema = '''
        partner_name:
            type: string
            required: true
            minlength: 5
        csrfmiddlewaretoken:
            type: string
            required: true
            minlength: 5
        firm_name:
            type: string
            required: true
            minlength: 6
        poc_email:
            type: string
            required: true
            regex: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
            minlength: 6
        poc_mobile:
            type: string
            required: true
            regex: '^\d{10}$'
        location_district:
            type: string
            required: true
        location_state:
            type: string
            required: true
        collaboration_sector:
            type: string
            required: true
        funding_stage_id:
            type: string
            required: true
        deal_size_range_min:
            type: string
            required: true
        deal_size_range_max:
            type: string
            required: true
        portfolio_size:
            type: string
            required: true
        company_website:
            type: string
            required: true
            regex: '(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
            minlength: 6
        linkedin_profile:
            type: string
            required: true
            regex: '(https?:\/\/(?:www\.|(?!www))[^\s\.]+\.[^\s]{2,}|www\.[^\s]+\.[^\s]{2,})'
            minlength: 6

        '''
        v = Validator()
        post_data = request.POST.dict()
        schema = yaml.load(request_schema, Loader=yaml.SafeLoader)
        if v.validate(post_data, schema):
                try:
                    new_vc_registration = VCRegistrations.objects.create(
                        partner_name = partner_name,
                        firm_name = firm_name,
                        deal_size_range_min = deal_size_range_min,
                        deal_size_range_max = deal_size_range_max,
                        portfolio_size = portfolio_size,
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
                except IntegrityError:
                    return JsonResponse(
                        {
                            'success': False,
                            'registration_id': "Failed",
                            'error': str(e),
                        })
        else:
                return JsonResponse(
                        {
                            'success': False,
                            'registration_id': "Failed",
                            'error': v.errors,
                        })
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
        
        
@login_required
def vc_registration_details(request):
    if request.user.user_role == 2:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            vc_id = data.get('vc_id',None)
            if not vc_id:
                return JsonResponse({'error': 'Invalid vc ID'}, status=400)
            # Fetch startup details based on startup_id
            print(vc_id)
            vc = VCRegistrations.objects.get(id=vc_id)
            # Construct HTML for the startup details
            html = f"""
                    <!--begin::Profile-->
                                                        <div class="d-flex gap-7 align-items-center">
                                                            <!--begin::Avatar-->
                                                            <div class="symbol symbol-circle symbol-100px">
                                                                <span class="symbol-label bg-light-success fs-1 fw-bolder">{vc.firm_name[:1]}</span>
                                                            </div>
                                                            <!--end::Avatar-->
                                                            <!--begin::Contact details-->
                                                            <div class="d-flex flex-column gap-2">
                                                                <!--begin::Name-->
                                                                <h3 class="mb-0">{vc.firm_name}</h3>
                                                                <!--end::Name-->
                                                                <!--begin::Email-->
                                                                <div class="d-flex align-items-center gap-2">
                                                                    <i class="ki-outline ki-sms fs-2"></i>
                                                                    <a href="#" class="text-muted text-hover-primary">{vc.area_of_interest.name}</a>
                                                                </div>
                                                                <!--end::Email-->
                                                                <!--begin::Phone-->
                                                                <div class="d-flex align-items-center gap-2">
                                                                    <i class="ki-outline ki-phone fs-2"></i>
                                                                    <a href="#" class="text-muted text-hover-primary">{vc.funding_stage.name}</a>
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

                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Partner Name</div>
                                                                        <div class="fw-bold fs-5">{vc.partner_name}</div>
                                                                    </div>
                                                                    <!--end::Company description-->
                                                                    <!--begin::market_size-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Market size</div>
                                                                        <div class="fw-bold fs-5">{vc.deal_size_range_min} - {vc.deal_size_range_max}</div>
                                                                    </div>
                                                                    <!--end::market_size-->
                                                                    <!--begin::funding_stage-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Portfolio size</div>
                                                                        <div class="fw-bold fs-5">{vc.portfolio_size}</div>
                                                                    </div>
                                                                    <!--end::funding_stage-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">District</div>
                                                                        <div class="fw-bold fs-5">{vc.district}</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">State</div>
                                                                        <div class="fw-bold fs-5">{vc.state}</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">LinkedIn</div>
                                                                        <a href="{vc.linkedin_profile}"><div class="fw-bold fs-5">{vc.linkedin_profile}</div></a>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Website</div>
                                                                        <a href="{vc.linkedin_profile}"><div class="fw-bold fs-5">{vc.company_website}</div></a>
                                                                    </div>
                    
                                                                </div>
                                                                <!--end::Additional details-->
                                                            </div>
                                                            <!--end:::Tab pane-->
                                                        </div>
                                                        <!--end::Tab content-->
            """
            # Send the HTML response to the JavaScript function
            return JsonResponse({'html': html})
        else:
            # Handle invalid request
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return render(request, 'common/not_found.html')
        