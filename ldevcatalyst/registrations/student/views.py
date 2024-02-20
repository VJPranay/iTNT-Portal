from django.shortcuts import render
from django.http import JsonResponse
from ..models import StudentRegistrations
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
from profiles.models import Student



@login_required
def student_registrations(request,registration_status=None):
    if registration_status is not None:
        student_registrations = StudentRegistrations.objects.filter(status=registration_status)
    else:
        student_registrations = StudentRegistrations.objects.all()
    student_registrations_list = []
    for x in student_registrations:
        temp = {
            'student_id' : x.id,
            'name':x.name,
            'institution':x.institution,
            'district' : x.district.name,
            'state':x.state.name,
           
            
            'created' : x.created,
        }
        student_registrations_list.append(temp)
    return render(request, 'dashboard/registrations/student/list.html',context={'student_registrations':student_registrations_list})


@login_required
def student_approve_registration(request):
    if request.method == 'POST':

        registration_id = request.POST.get('registration_id',None)
        if not registration_id:
            return JsonResponse({'success': False, 'error': 'Missing registration ID'}, status=400)
        else:
            try:
                registration = StudentRegistrations.objects.get(id=registration_id)
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
                student_profile=Student.objects.create(
                    user_id = user.id,
                    name = registration.name,
                    institution = registration.institution,
                    state = registration.state,
                    district = registration.district,
                    department=registration.department,
                    year_of_graduation=registration.year_of_graduation,
                    email=registration.email,
                    project_idea = registration.project_idea,
                )
                student_profile.save()
                for x in registration.area_of_interest.all():
                    student_profile.area_of_interest.add(x.id)
                    student_profile.save()
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
            except StudentRegistrations.DoesNotExist:
                print("error")
                return JsonResponse({'success': False, 'error': 'Registration not found'}, status=404)
    else:
        return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


def student_registration(request):
    if request.method == 'POST':
        print(request.POST)
        name = request.POST.get('name')
        institution_id = request.POST.get('institution')
        area_of_interest_id = request.POST.get('collaboration_sector')
        department_id = request.POST.get('department')
        year_of_graduation = request.POST.get('year_of_graduation')
        poc_email = request.POST.get('poc_email')
        state_id = request.POST.get('location_state')
        district_id = request.POST.get('location_district')
        project_idea = request.POST.get('project_idea')
        
        try:
            # Create a new StudentRegistrations object
            new_student_registration = StudentRegistrations.objects.create(
                name=name,
                institution_id=institution_id,
                department_id=department_id,
                year_of_graduation=year_of_graduation,
                email=poc_email,
                state_id=state_id,
                district_id=district_id,
                project_idea=project_idea,
            )
            new_student_registration.save()
            new_student_registration.area_of_interest.add(area_of_interest_id)
            # Save the object
            new_student_registration.save()
            # Save the object
           
            # Optionally, you can return a success response
            return JsonResponse(
                {
                    'success': True,
                    'registration_id': str(new_student_registration.registration_id),
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
        return render(request,'registrations/student_registration.html',context={ 
                         
        'student_types' : [
            {
                'student_id' : x.id,
                'student_value' : x.name,
            } for x in StudentRegistrations.objects.all()
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
        ],
        'departments' : [
            {
                'department_id' : x.id,
                'department_value' : x.name,
            } for x in Department.objects.all()
        ],
        'institutions' : [
            {
                'institution_id' : x.id,
                'institution_value' : x.name,
            } for x in Institution.objects.all()
        ]

        })
    


@login_required
def fetch_student_registration_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id',None)
        if not student_id:
            return JsonResponse({'error': 'Invalid student ID'}, status=400)
        # Fetch student details based on student_id
        print(student_id)
        student = StudentRegistrations.objects.get(id=student_id)
        # Construct HTML for the student details
        html = f"""
           													<!--begin::Profile-->
                                                            <div class="d-flex gap-7 align-items-center">
                                                                <!--begin::Avatar-->
                                                                <div class="symbol symbol-circle symbol-100px">
                                                                    <span class="symbol-label bg-light-success fs-1 fw-bolder">{student.name[:1]}</span>
                                                                </div>
                                                                <!--end::Avatar-->
                                                                <!--begin::Contact details-->
                                                                <div class="d-flex flex-column gap-2">
                                                                    <!--begin::Name-->
                                                                    <h3 class="mb-0">{student.name}</h3>
                                                                    <!--end::Name-->
                                                                    <!--begin::Email-->
                                                                    <div class="d-flex align-items-center gap-2">
                                                                        <i class="ki-outline ki-sms fs-2"></i>
                                                                        <a href="#" class="text-muted text-hover-primary">{student.email}</a>
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
                                                                            <div class="fw-bold fs-5">{student.state.name}</div>
                                                                        </div>
                                                                        <!--end::state-->
                                                                        <!--begin::district-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">District</div>
                                                                            <div class="fw-bold fs-5">{student.district.name}</div>
                                                                        </div>
                                                                        <!--end::district-->
                                                                        <!--begin::department_id-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Department ID</div>
                                                                            <div class="fw-bold fs-5">{student.department.name}</div>
                                                                        </div>
                                                                        <!--end::department_id-->
                                                                        <!--begin::year_of_graduation-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Year of Graduation</div>
                                                                            <div class="fw-bold fs-5">{student.year_of_graduation}</div>
                                                                        </div>
                                                                        <!--end::year_of_graduation-->
                                                                        <!--begin::email-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Email</div>
                                                                            <div class="fw-bold fs-5">{student.email}</div>
                                                                        </div>
                                                                        <!--end::email-->
                                                                        <!--begin::project_idea-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Project Idea</div>
                                                                            <div class="fw-bold fs-5">{student.project_idea}</div>
                                                                        </div>
                                                                        <!--end::project_idea-->
                                                                        <!--begin::area_of_interest_id-->
                                                                       <div class="d-flex flex-column gap-1">
                                                                        <div class="fw-bold text-muted">Area of Interest</div>
                                                                        <div class="fw-bold fs-5">
                                                                            
                                                                        </div>
                                                                    </div>
                                                                        <!--end::area_of_interest_id-->
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