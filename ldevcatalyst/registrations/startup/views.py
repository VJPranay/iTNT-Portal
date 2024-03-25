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
                'area_of_interest' : x.area_of_interest.name,
                'district' : x.district.name,
                'funding_stage' : x.funding_stage.name,
                'mobile' : x.mobile,
                'created' : x.created,
            }
            startup_registrations_list.append(temp)
        return render(request, 'dashboard/registrations/startup/list.html',context={'startup_registrations':startup_registrations_list})
    else:
        return render(request, 'common/not_found.html')


@login_required
def startup_approve_registration(request):
    if request.user.user_role == 2:
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
                        return JsonResponse({'success': True},status=200)
                    startup_profile = StartUp.objects.create(
                        user_id = user.id,
                        name = registration.name,
                        co_founder_count = registration.co_founder_count,
                        founder_names = registration.founder_names,
                        state = registration.state,
                        district = registration.district,
                        team_size = registration.team_size,
                        email = registration.email,
                        mobile = registration.mobile,
                        website = registration.website,
                        dpiit_number = registration.dpiit_number,
                        area_of_interest = registration.area_of_interest,
                        description = registration.description,
                        funding_stage = registration.funding_stage,
                        pitch_deck = registration.pitch_deck,
                        video_link = registration.video_link,
                        #market_size = registration.market_size,
                        required_amount = registration.required_amount,
                        founding_year = registration.founding_year,
                        #founding_experience = registration.founding_experience,
                        short_video = registration.short_video,
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
                    message['To'] = registration.email  # Add the additional email address
                    message['Subject'] = subject
                    message.attach(MIMEText(body, 'plain'))
                    with smtplib.SMTP_SSL(email_host, email_port) as server:
                        server.login(email_username, email_password)
                        server.sendmail(email_from, [registration.email], message.as_string())
                    return JsonResponse({'success': True})
                except StartUpRegistrations.DoesNotExist:
                    return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
        else:
            return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)
    else:
        return render(request, 'common/not_found.html')


def startup_registration(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        co_founder_count = request.POST.get('co_founder_count')
        founder_names = request.POST.get('founder_names')
        district_id = request.POST.get('location_district')
        state_id = request.POST.get('location_state')
        area_of_interest_id = request.POST.get('collaboration_sector')
        funding_stage_id = request.POST.get('funding_stage_id')
        reveune_stage_id = request.POST.get('reveune_stage_id')
        fund_raised_id = request.POST.get('fund_raised_id')
        fund_raised_input = request.POST.get('fund_raised_input')
        product_development_stage_id = request.POST.get('product_development_stage_id')
        primary_business_model_id = request.POST.get('primary_business_model_id')
        incubator = request.POST.get('incubator')
        customer_size = request.POST.get('customer_size')
        team_size = request.POST.get('team_size')
        dpiit_number = request.POST.get('dpiit_number')
        description = request.POST.get('description')
        pitch_deck = request.FILES.get('pitch_deck')
        company_logo = request.FILES.get('company_logo')
        product_development_stage_document = request.FILES.get('product_development_stage_document')
        video_link = request.POST.get('video_link')
        website = request.POST.get('company_website')
        required_amount = request.POST.get('required_amount')
        founding_year = request.POST.get('founding_year')
        company_linkedin = request.POST.get('company_linkedin')
        founder_names = json.loads(founder_names)
        if pitch_deck and pitch_deck.size > 25 * 1024 * 1024:  # 25 MB limit
            return JsonResponse({'success': False, 'error': 'Pitch deck PDF file size exceeds the limit of 25 MB.'}, status=400)
        if product_development_stage_document and product_development_stage_document.size > 25 * 1024 * 1024:  # 25 MB limit
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
        name:
            type: string
            required: true
        primary_business_model_id:
            type: string
            required: false
        fund_raised_id:
            type: string
            required: false
        fund_raised_input:
            type: string
            required: false
        incubator:
            type: string
            required: false
        customer_size:
            type: string
            required: false
        csrfmiddlewaretoken:
            type: string
            required: true
            minlength: 5
        co_founder_count:
            type: string
            required: true
        founder_names:
            type: string
            required: true
            minlength: 5
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
        team_size:
            type: string
            required: true
        dpiit_number:
            type: string
            required: false
        description:
            type: string
            required: true
        reveune_stage_id:
            type: string
            required: false
        product_development_stage_id:
            type: string
            required: true
        pitch_deck:
            type: string
            required: false
        product_development_stage_document:
            type: string
            required: false
        company_link:
            type: string
            required: false
        company_linkedin:
            type: string
            required: false
        video_link:
            type: string 
            required: false
        company_website:
            type: string
            required: false
        required_amount:
            type: string
            required: true
        founding_year:
            type: string
            required: true
        '''
        v = Validator()
        post_data = request.POST.dict()
        schema = yaml.load(request_schema, Loader=yaml.SafeLoader)
        if v.validate(post_data, schema):
            try:
                new_startup_registration = StartUpRegistrations.objects.create(
                    name = name,
                    #market_size = market_size,
                    required_amount = required_amount,
                    founding_year = founding_year,
                    #founding_experience = founding_experience,
                    #short_video = short_video_link,
                    co_founder_count = co_founder_count,
                    #founder_names = founder_names,
                    district_id = district_id,
                    state_id = state_id,
                    team_size = team_size,
                    primary_business_model_id = primary_business_model_id,
                    incubator = incubator,
                    customer_size = customer_size,
                    #email = email,
                    #mobile = mobile,
                    dpiit_number = dpiit_number,
                    area_of_interest_id = area_of_interest_id,
                    description = description,
                    funding_stage_id = funding_stage_id,
                    pitch_deck = pitch_deck,
                    company_logo = company_logo,
                    video_link = video_link,
                    website = website,
                    reveune_stage_id = reveune_stage_id,
                    product_development_stage_id = product_development_stage_id,
                    company_linkedin = company_linkedin,
                    product_development_stage_document = product_development_stage_document
                )
                new_startup_registration.save()
                for founder in founder_names:
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
                if fund_raised_input is not None:
                    new_startup_registration.fund_raised_value = fund_raised_input
                    new_startup_registration.save()
                else:
                    new_startup_registration.fund_raised_id = fund_raised_id
                    new_startup_registration.save()
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
                                                                                 'startup_years' : [
                                                                                     x for x in range(2009,2024)
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
            startup_id = data.get('startup_id',None)
            if not startup_id:
                return JsonResponse({'error': 'Invalid startup ID'}, status=400)
            # Fetch startup details based on startup_id
            startup = StartUpRegistrations.objects.get(id=startup_id)
            # Construct HTML for the startup details
            html = f"""
                                                                <!--begin::Profile-->
                                                        <div class="d-flex gap-7 align-items-center">
                                                            <!--begin::Avatar-->
                                                            <div class="symbol symbol-circle symbol-100px">
                                                                <span class="symbol-label bg-light-success fs-1 fw-bolder">"""+escape(startup.name[:1])+"""</span>
                                                            </div>
                                                            <!--end::Avatar-->
                                                            <!--begin::Contact details-->
                                                            <div class="d-flex flex-column gap-2">
                                                                <!--begin::Name-->
                                                                <h3 class="mb-0">"""+escape(startup.name)+"""</h3>
                                                                <!--end::Name-->
                                                                <!--begin::Email-->
                                                                <div class="d-flex align-items-center gap-2">
                                                                    <i class="ki-outline ki-sms fs-2"></i>
                                                                    <a href="#" class="text-muted text-hover-primary">"""+escape(startup.area_of_interest)+"""</a>
                                                                </div>
                                                                <!--end::Email-->
                                                                <!--begin::Phone-->
                                                                <div class="d-flex align-items-center gap-2">
                                                                    <i class="ki-outline ki-phone fs-2"></i>
                                                                    <a href="#" class="text-muted text-hover-primary">"""+escape(startup.funding_stage.name)+"""</a>
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
                                                                    <!--begin::Company description-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Pitch Deck</div>
<a href="{}" target="_blank" rel="noopener noreferrer">Click here to view the pitch deck PDF</a>
                                                                    </div>
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Description</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.description)+"""</div>
                                                                    </div>
                                                                    <!--end::Company description-->
                                                                    <!--begin::funding_stage-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Current funding stage</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.funding_stage.name)+"""</div>
                                                                    </div>
                                                                    <!--end::funding_stage-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Industry</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.area_of_interest.name)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Requried Amount</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.required_amount)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Founding year</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.founding_year)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Co-Founder team size </div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.co_founder_count)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Total team size</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.team_size)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::area_of_interest-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">State</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.state.name)+"""</div>
                                                                    </div>
                                                                    <!--end::area_of_interest-->
                                                                    <!--begin::district-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">City</div>
                                                                        <div class="fw-bold fs-5">"""+escape(startup.district.name)+"""</div>
                                                                    </div>
                                                                    <!--end::district-->
                                                                    <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Video</div>
                                                                        <a href="{}" target="_blank" rel="noopener noreferrer">Click here to view the video deck PDF</a>
                                                                    </div>
                    
                                                                </div>
                                                                <!--end::Additional details-->
                                                            </div>
                                                            <!--end:::Tab pane-->
                                                        </div>
                                                        <!--end::Tab content-->
            """.format(request.build_absolute_uri(startup.pitch_deck.url),escape(startup.video_link))
            # Send the HTML response to the JavaScript function
            
            return JsonResponse({'html': html})
        else:
            # Handle invalid request
            return JsonResponse({'error': 'Invalid request'}, status=400)
    else:
        return render(request, 'common/not_found.html')