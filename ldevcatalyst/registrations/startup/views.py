from django.shortcuts import render
from django.http import JsonResponse
from ..models import StartUpRegistrations,StartUpRegistrationsCoFounders
from datarepo.models import AreaOfInterest,State,PreferredInvestmentStage,District,RevenueStage,ProductDevelopmentStage,PrimaryBusinessModel,FundRaised
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
import random
import string
from django.http import JsonResponse
from profiles.models import User
from django.db.utils import IntegrityError
import smtplib
from ldevcatalyst import settings
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from profiles.models import StartUp
import json
import yaml
from cerberus import Validator
from django.db import IntegrityError
from django.utils.html import escape
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404


# access to only admin
@login_required
def startup_registrations(request,registration_status=None,area_of_interest=None):
    if request.user.user_role == 2:
        if registration_status is not None:
            startup_registrations = StartUpRegistrations.objects.filter(status=registration_status)
            if area_of_interest is not None:
                startup_registrations = startup_registrations.filter(area_of_interest__name=area_of_interest)
        else:
            startup_registrations = StartUpRegistrations.objects.all()
            if area_of_interest is not None:
                startup_registrations = startup_registrations.filter(area_of_interest__name=area_of_interest)
        startup_registrations_list = []
        for x in startup_registrations:
            temp = {
                'startup_id' : x.id,
                'name' : x.name,
                'area_of_interest' : x.area_of_interest,
                'district' : x.district,
                'funding_stage' : x.funding_stage,
                'mobile' : x.mobile,
                'created' : x.created,
            }
            startup_registrations_list.append(temp)
        return render(request, 'dashboard/registrations/startup/list.html',context={'startup_registrations':startup_registrations_list})
    else:
        return render(request, 'common/not_found.html')
    
from django.views.decorators.csrf import csrf_exempt

@login_required
def startup_approve_registration(request):
    # if request.user.user_role == 2:
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

                    # Check co_founders of the startup
                    try:
                        co_founders = StartUpRegistrationsCoFounders.objects.filter(startup_id=registration.id).first()
                        print(co_founders)
                        cofounder_names = ", ".join([x.name for x in StartUpRegistrationsCoFounders.objects.filter(startup_id=registration.id)])
                    except StartUpRegistrationsCoFounders.DoesNotExist:
                        co_founders = None

                    # Create user with the generated username and random password
                    try:
                        user = User.objects.create_user(username=username, password=password)
                        user.is_active = True
                        user.user_role = 6
                        user.email = co_founders.email
                        user.save()
                    except IntegrityError:
                        print('integirty error')
                        user = User.objects.get(username=username)
                        return JsonResponse({'success': True},status=200)
                    
                    startup_profile = StartUp.objects.create(
                        user_id = user.id,
                        company_name = registration.company_name,
                        co_founders_count = registration.co_founders_count,
                        founder_names = cofounder_names,
                        team_size = registration.team_size,
                        funding_request_amount = registration.funding_request_amount,
                        year_of_establishment = registration.year_of_establishment,
                        dpiit_number = registration.dpiit_number,
                        company_description = registration.company_description,
                        state_id = registration.state_id,
                        district_id = registration.district_id,
                        area_of_interest_id = registration.area_of_interest_id,
                        preferred_investment_stage_id = registration.preferred_investment_stage_id,
                        fund_raised_id = registration.fund_raised_id,
                        fund_raised_input = registration.fund_raised_input,
                        primary_business_model_id = registration.primary_business_model_id,
                        incubators_associated = registration.incubators_associated,
                        client_customer_size = registration.client_customer_size,
                        reveune_stage_id = registration.reveune_stage_id,
                        development_stage_id = registration. development_stage_id,
                        development_stage_document = registration.development_stage_document,
                        company_website = registration.company_website,
                        company_linkedin = registration.company_linkedin,
                        video_link = registration.video_link,
                        pitch_deck = registration.pitch_deck,
                        company_logo = registration.company_logo,
                        linkedin = co_founders.linkedin,
                        email = co_founders.email,
                        mobile = co_founders.mobile,
                        gender = co_founders.gender,
                        data_source = registration.data_source,
                        approved = True
                    )
                    startup_profile.save()
                   
                    print(startup_profile.id)
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
                    message = MIMEMultipart()
                    message['From'] = 'aso.itnt@tn.gov.in'
                    message['To'] = startup_profile.email  # Add the additional email address
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    with smtplib.SMTP_SSL(email_host, email_port) as server:
                        server.login(email_username, email_password)
                        server.sendmail(email_from, [startup_profile.email], message.as_string())
                    return JsonResponse({'success': True})
                except StartUpRegistrations.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
        else:
            return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    # else:
        # return render(request, 'common/not_found.html')


def startup_registration(request):
    if request.method == 'POST':
        company_name = request.POST.get('company_name')
        co_founders_count = request.POST.get('co_founders_count')
        team_size = request.POST.get('team_size')
        funding_request_amount = request.POST.get('funding_request_amount')
        year_of_establishment = request.POST.get('year_of_establishment')
        dpiit_number = request.POST.get('dpiit_number')
        company_description = request.POST.get('company_description')
        district_id = request.POST.get('district_id')
        state_id = request.POST.get('state_id')
        area_of_interest_id = request.POST.get('area_of_interest_id')
        preferred_investment_stage_id = request.POST.get('preferred_investment_stage_id')
        fund_raised_id = request.POST.get('fund_raised_id')
        fund_raised_input = request.POST.get('fund_raised_input')
        primary_business_model_id = request.POST.get('primary_business_model_id')
        incubators_associated = request.POST.get('incubators_associated')
        client_customer_size = request.POST.get('client_customer_size')
        reveune_stage_id = request.POST.get('reveune_stage_id')
        development_stage_id = request.POST.get('development_stage_id')
        development_stage_document = request.FILES.get('development_stage_document')
        company_website = request.POST.get('company_website')
        company_linkedin = request.POST.get('company_linkedin')
        video_link = request.POST.get('video_link')
        pitch_deck = request.FILES.get('pitch_deck')
        company_logo = request.FILES.get('company_logo')
        founder_names = request.POST.get('founder_names')
        founder_names = json.loads(founder_names)
        if pitch_deck and pitch_deck.size > 25 * 1024 * 1024:  # 25 MB limit
            return JsonResponse({'success': False, 'error': 'Pitch deck PDF file size exceeds the limit of 25 MB.'}, status=400)
        if development_stage_document and development_stage_document.size > 25 * 1024 * 1024:  # 25 MB limit
            return JsonResponse({'success': False, 'error': 'Product development stage document PDF file size exceeds the limit of 25 MB.'}, status=400)
        file_extension_validator = FileExtensionValidator(allowed_extensions=['pdf'])
        try:
            file_extension_validator(pitch_deck)
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        company_logo_extension_validator = FileExtensionValidator(allowed_extensions=['jpg','png','jpeg'])
        try:
            company_logo_extension_validator(company_logo)
        except ValidationError as e:
            return JsonResponse({'success': False, 'error': str(e)}, status=400)
        request_schema = '''
        csrfmiddlewaretoken:
            type: string
            required: true
            minlength: 5
        company_name:
            type: string
            required: true
        co_founders_count:
            type: string
            required: true
        team_size:
            type: string
            required: true
        funding_request_amount:
            type: string
            required: true
        year_of_establishment:
            type: string
            required: true
        dpiit_number:
            type: string
            required: false
        company_description:
            type: string
            required: true
        district_id:
            type: string
            required: true
        state_id:
            type: string
            required: true
        area_of_interest_id:
            type: string
            required: true
        preferred_investment_stage_id:
            type: string
            required: true
        fund_raised_id:
            type: string
            required: false
        fund_raised_input:
            type: string
            required: false
        primary_business_model_id:
            type: string
            required: true
        incubators_associated:
            type: string
            required: true
        client_customer_size:
            type: string
            required: true
        reveune_stage_id:
            type: string
            required: true
        development_stage_id:
            type: string
            required: true
        development_stage_document:
            type: string
            required: false
        founder_names:
            type: string 
            required: true
        company_website:
            type: string
            required: false
        company_linkedin:
            type: string
            required: false
        video_link:
            type: string
            required: false
        pitch_deck:
            type: string
            required: false
        company_logo:
            type: string
            required: false
        incubator:
            type: string
            required: false
        incubator_associated:
            type: string
            required: false
        '''
        v = Validator()
        post_data = request.POST.dict()
        schema = yaml.load(request_schema, Loader=yaml.SafeLoader)
        if v.validate(post_data, schema):
            try:
                new_startup_registration = StartUpRegistrations.objects.create(
                    company_name = company_name,
                    co_founders_count = co_founders_count,
                    team_size = team_size,
                    funding_request_amount = funding_request_amount,
                    year_of_establishment = year_of_establishment,
                    dpiit_number = dpiit_number,
                    district_id = district_id,
                    state_id = state_id,
                    area_of_interest_id = area_of_interest_id,
                    preferred_investment_stage_id = preferred_investment_stage_id,
                    fund_raised_id = fund_raised_id,
                    fund_raised_input = fund_raised_input,
                    primary_business_model_id = primary_business_model_id,
                    incubators_associated = incubators_associated,
                    client_customer_size = client_customer_size,
                    reveune_stage_id = reveune_stage_id,
                    company_description = company_description,
                    development_stage_id = development_stage_id,
                    development_stage_document = development_stage_document,
                    company_website = company_website,
                    company_linkedin = company_linkedin,
                    video_link = video_link,
                    pitch_deck = pitch_deck,
                    company_logo = company_logo,
                    
                )
                new_startup_registration.save()
                for founder in founder_names:
                    try:
                        name = founder.get('name')
                        email = founder.get('email')
                        mobile = founder.get('mobile')
                        gender = founder.get('gender')
                        linkedin = founder.get('linkedIn')
                        new_founder = StartUpRegistrationsCoFounders.objects.create(
                            startup_id = new_startup_registration.id,
                            name = name,
                            email = email,
                            mobile = mobile,
                            gender = gender,
                            linkedin = linkedin,
                        )
                        new_founder.save()
                    except Exception as e:
                        print('cofounder issue--> ',str(e))
                        return JsonResponse({'success': False,'registration_id': "Failed",'error': str(e),})
                
                
                
                registration = new_startup_registration
                registration.status = 'approved'
                registration.save()
                
                # Generate username from registration ID
                username = registration.registration_id
                    # Generate random 6-digit number
                password = ''.join(random.choices(string.digits, k=6))

                    # Check co_founders of the startup
                try:
                    co_founders = StartUpRegistrationsCoFounders.objects.filter(startup_id=registration.id).first()
                    
                except StartUpRegistrationsCoFounders.DoesNotExist:
                    co_founders = None
                    # Create user wit the generated username and random password
                try:
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.user_role = 6
                    user.email = co_founders.email
                    user.save()
                except IntegrityError:
                    pass
               
                startup_profile = StartUp.objects.create(
                        user_id = user.id,
                        company_name = registration.company_name,
                        co_founders_count = registration.co_founders_count,
                        founder_names = co_founders.name,
                        team_size = registration.team_size,
                        funding_request_amount = registration.funding_request_amount,
                        year_of_establishment = registration.year_of_establishment,
                        dpiit_number = registration.dpiit_number,
                        company_description = registration.company_description,
                        state_id = registration.state_id,
                        district_id = registration.district_id,
                        area_of_interest_id = registration.area_of_interest_id,
                        preferred_investment_stage_id = registration.preferred_investment_stage_id,
                        fund_raised_id = registration.fund_raised_id,
                        fund_raised_input = registration.fund_raised_input,
                        primary_business_model_id = registration.primary_business_model_id,
                        incubators_associated = registration.incubators_associated,
                        client_customer_size = registration.client_customer_size,
                        reveune_stage_id = registration.reveune_stage_id,
                        development_stage_id = registration. development_stage_id,
                        development_stage_document = registration.development_stage_document,
                        company_website = registration.company_website,
                        company_linkedin = registration.company_linkedin,
                        video_link = registration.video_link,
                        pitch_deck = registration.pitch_deck,
                        company_logo = registration.company_logo,
                        linkedin = co_founders.linkedin,
                        email = co_founders.email,
                        mobile = co_founders.mobile,
                        gender = co_founders.gender,
                        data_source = registration.data_source,
                        approved = True
                    )
                startup_profile.save()
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
                message = MIMEMultipart()
                message['From'] = 'aso.itnt@tn.gov.in'
                message['To'] = startup_profile.email  # Add the additional email address
                message['Subject'] = subject
                message.attach(MIMEText(body, 'plain'))
                with smtplib.SMTP_SSL(email_host, email_port) as server:
                    server.login(email_username, email_password)
                    server.sendmail(email_from, [startup_profile.email], message.as_string())
                return JsonResponse(
                    {
                        'success': True,
                        'registration_id': str(new_startup_registration.registration_id),
                    }
                    )
            except IntegrityError as e:
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
        return render(request,'registrations/startup_registration.html',context={ 
                                                                                 'year_of_establishment_years' : [
                                                                                     x for x in range(2009,2025)
                                                                                 ],
         
        'preferred_investment_stages' : [
            {
                'id' : x.id,
                'value' : x.name,
            } for x in PreferredInvestmentStage.objects.all().order_by('serial')
        ],
        'fundraised_values' : [
            {
                'id' : x.id,
                'value' : x.name,
            } for x in FundRaised.objects.all().order_by('serial')
        ],
        'primary_business_models' : [
            {
                'id' : x.id,
                'value' : x.name,
            } for x in PrimaryBusinessModel.objects.all().order_by('serial')
        ],
        'revenue_stages' : [
            {
                'id' : x.id,
                'value' : x.name,
            } for x in RevenueStage.objects.all().order_by('serial')
        ],
        'product_development_stages' : [
            {
                'id' : x.id,
                'value' : x.name,
                'description' : x.description
            } for x in ProductDevelopmentStage.objects.all().order_by('serial')
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
        ],
        'area_of_interests' : [
            {
                'area_of_interest_id' : x.id,
                'area_of_interest_value' : x.name,
            } for x in AreaOfInterest.objects.filter(is_approved=True)    
        ]})
        
        
@login_required
def fetch_startup_registration_details(request):
    if request.user.user_role == 2:
        if request.method == 'POST':
            data = json.loads(request.body.decode('utf-8'))
            startup_id = data.get('startup_id', None)
            if not startup_id:
                return JsonResponse({'error': 'Invalid startup ID'}, status=400)

            # Fetch startup details based on startup_id
            startup = get_object_or_404(StartUpRegistrations, id=startup_id)

            # Construct HTML for the startup details
            html = f"""
                <!--begin::Profile-->
                <div class="d-flex gap-7 align-items-center">
                    <!--begin::Logo-->
                    <img src="{startup.company_logo.url if startup.company_logo else ''}" alt="{escape(startup.name)}" style="width: 150px;height: auto;" >
                    <!--end::Logo-->
                    <!--begin::Contact details-->
                    <div class="d-flex flex-column gap-2">
                        <!--begin::Name-->
                        <h3 class="mb-0">{escape(startup.name)}</h3>
                        <!--end::Name-->
                        <!--begin::Email-->
                        <div class="d-flex align-items-center gap-2">
                            <i class="ki-outline ki-sms fs-2"></i>
                            <a href="#" class="text-muted text-hover-primary">{escape(startup.required_amount)}</a>
                        </div>
                        <!--end::Email-->
                        <!--begin::Phone-->
                        <div class="d-flex align-items-center gap-2">
                            <i class="ki-outline ki-phone fs-2"></i>
                            <a href="#" class="text-muted text-hover-primary">{escape(startup.funding_stage.name if startup.funding_stage else '')}</a>
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
                            <i class="ki-outline ki-home fs-4 me-1"></i>Information
                        </a>
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
                            <!--begin::Company description-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Funding request amount</div>
                                <div class="fw-bold fs-5">{escape(startup.required_amount)}</div>
                            </div>
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Description</div>
                                <div class="fw-bold fs-5">{escape(startup.description)}</div>
                            </div>
                            <!--end::Company description-->
                            <!--begin::Required Amount-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Area of Interest</div>
                                <div class="fw-bold fs-5">{escape(startup.area_of_interest.name if startup.area_of_interest else '')}</div>
                            </div>
                            <!--begin::Preferred Investment Stage-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Preferred Investment Stage</div>
                                <div class="fw-bold fs-5">{escape(startup.funding_stage.name if startup.funding_stage else '')}</div>
                            </div>
                            <!--end::Preferred Investment Stage-->
                            <!--begin::Revenue Stage-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Revenue Stage</div>
                                <div class="fw-bold fs-5">{escape(startup.reveune_stage.name if startup.reveune_stage else '')}</div>
                            </div>
                            <!--end::Revenue Stage-->
                            <!--begin::Startup Stage-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Startup Stage</div>
                                <div class="fw-bold fs-5">{escape(startup.product_development_stage.name if startup.product_development_stage else '')}</div>
                            </div>
                            <!--end::Startup Stage-->
                            <!--begin::Proof of Document-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Proof of Document</div>
                                 <a href="/innovation-portal/media/{startup.product_development_stage_document.url.split('/media/', 1)[1] if startup.product_development_stage_document else '#'}" target="_blank" rel="noopener noreferrer">Click here to view</a>

                            </div>
                            <!--end::Proof of Document-->
                            <!--begin::Video Link-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Video Link</div>
                                <a href="{startup.video_link}" target="_blank" rel="noopener noreferrer">Click here to view</a>

                            </div>
                            <!--end::Video Link-->
                            <!--begin::Pitch Deck-->
                            <div class="d-flex flex-column gap-1">
                                <div class="fw-bold text-muted">Pitch Deck</div>
                                <a href="/innovation-portal/media/{startup.pitch_deck.url.split('/media/', 1)[1] if startup.pitch_deck else '#'}" target="_blank" rel="noopener noreferrer">Click here to view</a> 
                            </div>
                            <!--end::Pitch Deck-->
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