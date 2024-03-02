from django.shortcuts import render
from django.http import JsonResponse
from ..models import ResearcherRegistrations, PatentInfo, PublicationInfo
from datarepo.models import AreaOfInterest,State,Department,District,Institution
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
import json
from registrations.models import PatentInfo,PublicationInfo
from profiles.models import Researcher,Patent,Publication
import yaml
from cerberus import Validator
from django.db import IntegrityError
from django.utils.html import escape
from django.db import transaction
from django.template.loader import render_to_string

@login_required
def sme_registrations(request,registration_status=None):
    if registration_status is not None:
        sme_registrations = ResearcherRegistrations.objects.filter(status=registration_status)
    else:
        sme_registrations = ResearcherRegistrations.objects.all()
    sme_registrations_list = []
    for x in sme_registrations:
        temp = {
            'sme_id' : x.id,
            'name' : x.name,
            'area_of_interest' : x.area_of_interest,
            'department':x.department.name,
            'state':x.state.name,
            'district' : x.district.name,
            'created' : x.created,
            'status' : x.status,
        }
        sme_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/sme/list.html',context={'sme_registrations':sme_registrations_list})


@login_required
def sme_approve_registrations(request):
    if request.method == 'POST':
        registration_id = request.POST.get('registration_id', None)
        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = ResearcherRegistrations.objects.get(id=registration_id)

                # Generate Username from Registration Id
                username = registration.registration_id

                # Generating Random 6 digit number
                password = ''.join(random.choices(string.digits, k=6))

                # Create User with Username and random Password
                try:
                    user = User.objects.create_user(username=username, password=password)
                    user.is_active = True
                    user.user_role = 5
                    user.email = registration.email
                    user.save()
                except IntegrityError:
                    user = User.objects.get(username=username)
                    return JsonResponse({'success': True}, status=200)

                # Create new publication
                publication_info = registration.publications
                new_publication = Publication.objects.create(
                        user_id=user.id,
                        title=publication_info.title,
                        paper_link=publication_info.paper_link,
                        journal=publication_info.journal,
                    )


                # Create SME profile
                sme_profile = Researcher.objects.create(
                    user_id=user.id,
                    name=registration.name,
                    department=registration.department,
                    institution=registration.institution,
                    district=registration.district,
                    state=registration.state,
                    email=registration.email,
                    mobile=registration.mobile,
                    highest_qualification=registration.highest_qualification,
                    created=registration.created,
                    updated=registration.updated,
                    publications=new_publication
                )
                sme_profile.save()

                # Add area of interest
                sme_profile.area_of_interest.set(registration.area_of_interest.all())

                # Associate patents with SME profile
                for x in registration.patents.all():
                    new_patent = Patent.objects.create(
                        user_id=user.id,
                        number=x.number,
                        title=x.title,
                        inventors=x.inventors,
                        filing_date=x.filing_date,
                        status=x.status
                    )
                    new_patent.save()
                    sme_profile.patents.add(new_patent)
                    sme_profile.save()

                # Change registration status to approved
                registration.status = 'approved'
                registration.save()

                email_host = settings.email_host
                email_port = settings.email_port
                email_username = settings.email_username
                email_password = settings.email_password
                email_from = settings.email_from
                subject = 'You iTNT SME registration has been approved'
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
                return JsonResponse({'success': True})
            except ResearcherRegistrations.DoesNotExist:
                return JsonResponse({'status': False, 'error': 'Registration not found'}, status=404)
    else:
        return JsonResponse({'status': False, 'error': 'Method not allowed'}, status=405)
                
        
def sme_registration(request):
    if request.method == 'POST':
        # Retrieve data from the POST request
        name = request.POST.get('name')
        institution_id = request.POST.get('institution')
        department_id = request.POST.get('department')
        district_id = request.POST.get('location_district')
        state_id = request.POST.get('location_state')
        email = request.POST.get('email')
        area_of_interest_id = request.POST.get('collaboration_sector')
        mobile = request.POST.get('mobile')
        highest_qualification = request.POST.get('highest_qualification')
        # Patent
        patent_data = request.POST.get('patents')

        # Publications
        title = request.POST.get('publication_title')
        paper_link = request.POST.get('paper_link')
        journal = request.POST.get('journal')
        institution_info = None
        department_info = None
        try:
            institution_info = Institution.objects.get(id=institution_id)
        except Institution.DoesNotExist:
            pass
        try:
            department_info = Department.objects.get(id=department_id)
        except Department.DoesNotExist:
            pass
        if area_of_interest_id.replace(" ",'') == '' or highest_qualification.replace(" ",'') == '':
            return JsonResponse(
                    {
                        'success': False,
                        'registration_id': "Failed",
                        'error': "area of interest field cant be empty",
                    })
        if highest_qualification.replace(" ",'').lower() =='ph.d':
            if title.replace(" ",'') == '' or journal.replace(" ",'') == '':
                return JsonResponse(
                    {
                        'success': False,
                        'registration_id': "Failed",
                        'error': "publication details cant be empty",
                    })
        request_schema='''
        name:
            type: string
            required: true

        highest_qualification_input:
            type: string
            required: false
        
        collaboration_sector_other:
            type: string
            required: false

            
        csrfmiddlewaretoken:
            type: string
            required: true


        institution:
            type: string
            required: true

        department:
            type: string
            required: true

        location_state:
            type: string
            required: true

        location_district:
            type: string
            required: true

        email:
            type: string
            required: true
            regex: '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
           
        collaboration_sector:
            type: string
            required: true
        
        mobile:
            type: string
            required: true
            regex: '^\d{10}$'

        highest_qualification:
            type: string
            required: true

        publication_title:
            type: string
            required: false

        paper_link:
            type: string
            required: false

        journal:
            type: string
            required: false

        patents:
            type: string
            required: false
    
        filing_date[]:
            type: string
            required: false
                    
        inventors[]:
            type: string
            required: false

        number[]:
            type: string
            required: false
        
        status[]:
            type: string
            required: false

        title[]:
            type: string
            required: false
        '''
        v=Validator()
        post_data = request.POST.dict()
        schema=yaml.load(request_schema, Loader=yaml.SafeLoader)     
        if v.validate(post_data,schema):   
            try:

                # Create ResearcherRegistrations object
                new_sme_registration = ResearcherRegistrations.objects.create(
                    name=name,
                    institution_id=institution_info.id,
                    department_id=department_info.id,
                    district_id=district_id,
                    state_id=state_id,
                    mobile=mobile,
                    email=email,
                    highest_qualification=highest_qualification,
                    #patents_id=new_patent_info.id
                )
                if title.replace(" ",'') != '' or journal.replace(" ",'') != '':
                    new_publication_i = PublicationInfo.objects.create(
                        title=title,
                        paper_link=paper_link,
                        journal=journal
                    )
                    new_publication_i.save()
                    new_sme_registration.publications_id = new_publication_i.id
                    new_sme_registration.save()
                patent_data = json.loads(patent_data)
                for patent in patent_data:
                    if patent['title'].replace(" ",'') != '' or patent['inventors'].replace(" ",'') != '':
                        new_patent_info = PatentInfo.objects.create(
                        number=patent['number'],
                        title=patent['title'],
                        inventors=patent['inventors'],
                        filing_date=patent['filing_date'],
                        status=patent['status'])
                        new_patent_info.save()
                        new_sme_registration.patents.add(new_patent_info)
                    
                try:
                    area_of_interest_id_int = int(area_of_interest_id)
                    area_of_interest_info = AreaOfInterest.objects.get(id=area_of_interest_id_int)
                    new_sme_registration.area_of_interest.add(area_of_interest_id_int)
                except (ValueError, AreaOfInterest.DoesNotExist):
                    area_of_interest_info = AreaOfInterest.objects.create(name=area_of_interest_id,is_approved=False)
                    area_of_interest_info.save()
                    new_sme_registration.area_of_interest.add(area_of_interest_info)
                new_sme_registration.save()

                return JsonResponse({
                    'success': True,
                    'registration_id': str(new_sme_registration.registration_id),
                }) 
            except IntegrityError as e :
                return JsonResponse({
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
        # Return the initial form data
        return render(request, 'registrations/sme_registration.html', context={
            'departments': [
                {'department_id': x.id, 'department_name': x.name} for x in Department.objects.all().order_by('name')
            ],
            'districts': [
                {'district_id': x.id, 'district_name': x.name} for x in District.objects.all().order_by('name')
            ],
            'states': [
                {'state_id': x.id, 'state_name': x.name} for x in State.objects.all().order_by('name')
            ],
            'area_of_interests': [
                {'area_of_interest_id': x.id, 'area_of_interest_name': x.name} for x in AreaOfInterest.objects.filter(is_approved=True).order_by('name')
            ],
        })
    

@login_required
def fetch_sme_registration_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        sme_id = data.get('sme_id', None)
        if not sme_id:
            return JsonResponse({'error': 'Invalid sme ID'}, status=400)
        
        sme = ResearcherRegistrations.objects.get(id=sme_id)
        patents = PatentInfo.objects.filter(id__in=sme.patents.values_list('id', flat=True))
        try:
            publication = PublicationInfo.objects.get(id=sme.publications_id)
        except PublicationInfo.DoesNotExist:
            publication = None
        
        context = {
            'sme': sme,
            'patents': patents,
            'publication': publication,
        }
        
        html = render_to_string('dashboard/profiles/sme/sme_details_template.html', context)
        return JsonResponse({'html': html})
    else:
        return JsonResponse({'error': 'Invalid request'}, status=400)