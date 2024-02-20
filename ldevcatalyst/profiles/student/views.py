from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from datarepo.models import AreaOfInterest
from django.template.defaultfilters import pluralize
from profiles.models import Student
from django.http import HttpResponseRedirect
from django.urls import reverse
from datarepo.models import AreaOfInterest
from profiles.models import StartUp
from django.db.models import Count
from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST

from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
import json

from ..models import Student
# Create your views here.


@login_required
def student_list(request):
    # Get all areas of interests with profile count
    areas_q = AreaOfInterest.objects.all()
    areas_list = []
    for x in areas_q:
        temp = {
            'id': x.id,
            'name': x.name,
            'count': Student.objects.filter(
                area_of_interest=x  # Adjusted to match the many-to-many relationship
            ).count()
        }
        areas_list.append(temp)
    template_data = {
        'areas_list': areas_list
    }
    return render(request, 'dashboard/profiles/vc/student/list.html', context=template_data)



@require_POST
@login_required
def fetch_student_profiles(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        area_of_interest_ids = data.get('area_of_interest', None)
        if not area_of_interest_ids:
            return JsonResponse({'error': 'Area of Interest ID(s) are required'}, status=400)
        student_profiles_q = Student.objects.filter(
            area_of_interest__id=area_of_interest_ids
        ) # Ensure unique student profiles
        
        student_profiles = []
        for profile in student_profiles_q:
            student_profiles.append({
                'student_id': profile.id,
                'name': profile.name,
                'department': profile.department.name,
            })
        return JsonResponse(student_profiles, safe=False)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)
    
@login_required
def fetch_student_details(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        student_id = data.get('student_id',None)
        if not student_id:
            return JsonResponse({'error': 'Invalid student ID'}, status=400)
        # Fetch startup details based on startup_id
        print(student_id)
        student = Student.objects.get(id=student_id)
        # Construct HTML for the startup details
        html = f"""
           													<!--begin::Profile-->
                                                            <div class="d-flex gap-7 align-items-center">
                                                                <!--begin::Avatar-->
                                                                <div class="symbol symbol-circle symbol-200px">
                                                                    <span class="symbol-label bg-light-success fs-1 fw-bolder">{student.user}</span>
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
                                                                            <div class="fw-bold fs-5">{student.state}</div>
                                                                        </div>
                                                                        <!--end::state-->
                                                                        <!--begin::district-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">District</div>
                                                                            <div class="fw-bold fs-5">{student.district}</div>
                                                                        </div>
                                                                        <!--end::district-->
                                                                        <!--begin::department_id-->
                                                                        <div class="d-flex flex-column gap-1">
                                                                            <div class="fw-bold text-muted">Department ID</div>
                                                                            <div class="fw-bold fs-5">{student.department}</div>
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
                                                                            <div class="fw-bold text-muted">Institution</div>
                                                                            <div class="fw-bold fs-5">{student.institution}</div>
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
                                                                            <div class="fw-bold text-muted">Area{'s' if student.area_of_interest.count() > 1 else ''} of Interest:</div>
                                                                            {student.area_of_interest}
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
    