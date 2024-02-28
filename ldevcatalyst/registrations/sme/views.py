from django.shortcuts import render
from django.http import JsonResponse
from ..models import ResearcherRegistrations
from datarepo.models import AreaOfInterest,State,Department,District,Institution
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
from registrations.models import PatentInfo,PublicationInfo
from profiles.models import Researcher,Patent,Publication
import yaml
from cerberus import Validator
from django.db import IntegrityError
from django.utils.html import escape
from django.db import transaction

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
        }
        sme_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/sme/list.html',context={'sme_registrations':sme_registrations_list})


@login_required
def sme_approve_registrations(request):
    if request.method=='POST':
        registration_id=request.POST.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success':False,'error':'Missing registration ID'},status=400)
        else:
            try:
                registration=ResearcherRegistrations.objects.get(id=registration_id)

                
                #Generate Userneme from Registaration Id
                username=registration.registration_id
  
                
                #Generating Randon 6 digit number
                password="".join(random.choices(string.digits,k=6))

                
                #Create User with Username and random Password
                try:
                    user=User.objects.create_user(username=username,password=password)
                    user.is_active=True
                    user.user_role = 5
                    user.email = registration.email
                    user.save()
                except IntegrityError :
                    user = User.objects.get(username=username)
                    return JsonResponse({'success': True},status=200)
                

                patent_q = PatentInfo.objects.get(id=registration.patents_id)

                new_patent= Patent.objects.create(
                        user_id = user.id,
                        number=patent_q.number,
                        title=patent_q.title,
                        inventors=patent_q.title,
                        filing_date=patent_q.filing_date,
                        status=patent_q.status
                
                    )
                new_patent.save()

                publication_info_q = PublicationInfo.objects.get(id=registration.publications_id)

                new_publication_info = Publication.objects.create(
                    user_id=user.id,
                    title=publication_info_q.title,
                    paper_link=publication_info_q.paper_link,
                    journal=publication_info_q.journal,
                )
                new_publication_info.save()
                
                sme_profile=Researcher.objects.create(
                            user_id =user.id,
                            name = registration.name,
                            department = registration.department,
                            institution = registration.institution,
                            district = registration.district,
                            state = registration.state,
                            email = registration.email,
                            mobile = registration.mobile,
                            highest_qualification = registration.highest_qualification,
                            created = registration.created,
                            updated = registration.updated,
                            patents_id=new_patent.id,
                            publications_id=new_publication_info.id
                )
                sme_profile.save()
                for x in registration.area_of_interest.all():
                    sme_profile.area_of_interest.add(x.id)
                    sme_profile.save()
                registration.status='approved'
                registration.save()

                email_host='mail.ldev.in'
                email_port = 465
                email_username = 'itntadmin@ldev.in'
                email_password = 'Pranay123@'
                subject = 'You iTNT registration has been approved'
                body = f'''
                        Username: {user.username}
                        Password: {password}
                        Login URL: http://innovationportal.tnthub.org.ldev.in/dashboard
                        '''


                message=MIMEMultipart()
                message['From']=email_username
                message['To']=registration.email
                message['Subject']=subject
                message.attach(MIMEText(body,'plain'))
                with smtplib.SMTP_SSL(email_host,email_port) as server:
                    server.login(email_username,email_password)   
                    server.sendmail(email_username,[registration.email],message.as_string())
 
                return JsonResponse({'success':True}) 
            except  ResearcherRegistrations.DoesNotExist:
                return JsonResponse({'status':False,'error':'Registration not found'},status=404)
    else:
        return JsonResponse({'status':False,'error':'Method not allowed'},status=405)
                 
                
                
        
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
                
                new_publication_info = PublicationInfo.objects.create(
                    title=title,
                    paper_link=paper_link,
                    journal=journal
                )



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
                    #patents_id=new_patent_info.id,
                    publications_id=new_publication_info.id,
                )
                patent_data = json.loads(patent_data)
                for patent in patent_data:
                    new_patent_info = PatentInfo.objects.create(
                        number=patent['number'],
                        title=patent['title'],
                        inventors=patent['inventors'],
                        filing_date=patent['filing_date'],
                        status=patent['status']
                    )
                    new_patent_info.save()
                    new_sme_registration.patents.add(new_patent_info)
                try:
                    area_of_interest_id_int = int(area_of_interest_id)
                    area_of_interest_info = AreaOfInterest.objects.get(id=area_of_interest_id_int)
                    new_sme_registration.area_of_interest.add(area_of_interest_id_int)
                except (ValueError, AreaOfInterest.DoesNotExist):
                    area_of_interest_info = AreaOfInterest.objects.create(name=area_of_interest_id)
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
                {'department_id': x.id, 'department_name': x.name} for x in Department.objects.all()
            ],
            'districts': [
                {'district_id': x.id, 'district_name': x.name} for x in District.objects.all()
            ],
            'states': [
                {'state_id': x.id, 'state_name': x.name} for x in State.objects.all()
            ],
            'area_of_interests': [
                {'area_of_interest_id': x.id, 'area_of_interest_name': x.name} for x in AreaOfInterest.objects.all()
            ],
        })
    

@login_required
def fetch_sme_registration_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        sme_id = data.get('sme_id',None)
        if not sme_id:
            return JsonResponse({'error': 'Invalid sme ID'}, status=400)
        # Fetch sme details based on sme_id
        sme = ResearcherRegistrations.objects.get(id=sme_id)
        patent=PatentInfo.objects.get(id=sme.patents_id)
        publication=PublicationInfo.objects.get(id=sme.publications_id)
        area_of_interest_html = ""
        for interest in sme.area_of_interest.all():
            area_of_interest_html += f"{interest.name}"
        # Construct HTML for the sme details
        html = f"""
                                   
                                    <!--begin::Profile-->
                                    <div class="d-flex gap-7 align-items-center">
                                        <!--begin::Avatar-->
                                        <div class="symbol symbol-circle symbol-100px">
                                            <span class="symbol-label bg-light-success fs-1 fw-bolder">"""+escape(sme.name[:1])+"""</span>
                                        </div>
                                        <!--end::Avatar-->
                                        <!--begin::Contact details-->
                                        <div class="d-flex flex-column gap-2">
                                            <!--begin::Name-->
                                            <h3 class="mb-0">"""+escape(sme.name) + """</h3>
                                            <!--end::Name-->
                                            <!--begin::Email-->
                                            <div class="d-flex align-items-center gap-2">
                                                <i class="ki-outline ki-sms fs-2"></i>
                                                <a href="#" class="text-muted text-hover-primary">"""+escape(sme.email) + """</a>
                                            </div>
                                            <!--end::Email-->
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
                                                    <div class="fw-bold fs-5">"""+escape(sme.state.name) + """</div>
                                                </div>
                                                <!--end::state-->
                                                <!--begin::district-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">District</div>
                                                    <div class="fw-bold fs-5">"""+escape(sme.district.name) + """</div>
                                                </div>
                                                <!--end::district-->
                                                <!--begin::department-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Department</div>
                                                    <div class="fw-bold fs-5">"""+escape(sme.department.name) + """</div>
                                                </div>
                                                <!--end::department-->
                                                <!--begin::institution-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Institution</div>
                                                    <div class="fw-bold fs-5">"""+escape(sme.institution.name) + """</div>
                                                </div>
                                                <!--end::institution-->
                                                <!--begin::mobile-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Mobile</div>
                                                    <div class="fw-bold fs-5">"""+escape(sme.mobile) + """</div>
                                                </div>
                                                <!--end::mobile-->
                                                <!--begin::highest_qualification-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Highest Qualification</div>
                                                    <div class="fw-bold fs-5">"""+escape(sme.highest_qualification) + """</div>
                                                </div>
                                              <!--end::highest_qualification-->

                                                 <!--begin::area_of_interest-->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Area of Interest</div>
                                                    <div class="fw-bold fs-5">"""+escape(area_of_interest_html) + """</div>
                                                </div>
                                                <!--end::area_of_interest-->
                        
                                                <!--end::mobile-->
                                                <!--end::picture-->
                                                
                                                <!-- begin::number -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Patent Number</div>
                                                    <div class="fw-bold fs-5">"""+escape(patent.number) + """</div>
                                                </div>
                                                <!-- end::number-->

                                                <!-- begin::title -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Title</div>
                                                    <div class="fw-bold fs-5">"""+escape(patent.title) + """</div>
                                                </div>
                                                <!-- end::title -->

                                                <!-- begin::inventors -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Inventors</div>
                                                    <div class="fw-bold fs-5">"""+escape(patent.inventors) + """</div>
                                                </div>
                                                <!-- end::inventors -->

                                                <!-- begin::filing_date -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Filing Date</div>
                                                    <div class="fw-bold fs-5">"""+escape(patent.filing_date) + """</div>
                                                </div>
                                                <!-- end::filing_date -->

                                                <!-- begin::status -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Status</div>
                                                    <div class="fw-bold fs-5">"""+escape(patent.status) + """</div>
                                                </div>
                                                <!-- end::status -->

                                                <!-- begin::paper_title -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Paper Title</div>
                                                    <div class="fw-bold fs-5">"""+escape(publication.title) + """</div>
                                                </div>
                                                <!-- end::paper_title -->

                                                <!-- begin::paper_link -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Paper Link</div>
                                                    <div class="fw-bold fs-5">"""+escape(publication.paper_link) + """</div>
                                                </div>
                                                <!-- end::paper_link -->

                                                <!-- begin::journal -->
                                                <div class="d-flex flex-column gap-1">
                                                    <div class="fw-bold text-muted">Journal</div>
                                                    <div class="fw-bold fs-5">"""+escape(publication.journal) + """</div>
                                                </div>
                                                <!-- end::journal -->

                                                <!--begin::Additional details-->    

                                                
                                               
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