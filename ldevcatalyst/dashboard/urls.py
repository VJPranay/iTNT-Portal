from django.urls import path
from .views import custom_login,dashboard_index,logout
from registrations.industry.views import industry_registrations,industry_approve_registration
from registrations.startup.views import startup_registrations,startup_approve_registration
from registrations.vc.views import vc_registrations,vc_approve_registration
from registrations.student.views import student_registrations, student_approve_registration
from registrations.sme.views import sme_registrations,sme_approve_registration
from mentor.views import mentor_registration,mentor_approve_registration
# registrations
from dashboard.registrations.list_view import StartUpRegistrationsListView,ResearcherRegistrationsListView, StudentRegistrationsListView,VCRegistrationsListView, IndustryRegistrationsListView,MentorRegistrationsListView
from dashboard.registrations.registration_details import startup_registration_details,Researcher_registration_details, student_registration_details,vc_registration_details, industry_registration_details,mentor_registration_details
# profiles
from dashboard.profiles.list_view import StartUpListView, ResearcherListView, StudentListView, VCListView, IndustryListView
from dashboard.profiles.profile_details import startup_profile_details, researcher_profile_details, student_profile_details, vc_profile_details, industry_profile_details



urlpatterns = [
    path('', custom_login, name='login'),
    path('logout', logout, name='logout'),
    path('index', dashboard_index, name='dashboard_index'),
    path('registrations/industry/<str:registration_status>/', industry_registrations, name='industry_registrations'),
    path('registrations/startup/<str:registration_status>/', startup_registrations, name='startup_registrations'),
    path('registrations/startup/<str:area_of_interest>', startup_registrations, name='startup_registrations_cat'),
    path('registrations/sme/<str:area_of_interest>', sme_registrations, name='researcher_registrations_cat'),
    path('registrations/vc/<str:registration_status>/', vc_registrations, name='vc_registrations'),
    path('registrations/mentor/<str:registration_status>/', mentor_registration, name='mentor_registration'),

   
   
    #student
    path('registrations/student/<str:registration_status>/', student_registrations, name='student_registrations'),



    #sme
    path('registrations/sme/<str:registration_status>/', sme_registrations, name='sme_registrations'),
        

    # sme registrations
    path('registrations/v2/researchers', ResearcherRegistrationsListView.as_view(), name='researcher_registrations_list'),
    path('registrations/v2/researcher/<int:pk>', Researcher_registration_details, name='researcher_registration_details'),
    path('registrations/sme/approve_registration', sme_approve_registration, name='sme_approve_registration'),

    
    # startup registrations
    path('registrations/v2/startups', StartUpRegistrationsListView.as_view(), name='startup_registrations_list'),
    path('registrations/v2/startup/<int:pk>', startup_registration_details, name='startup_registration_details'),
    path('registrations/startup/approve_registration', startup_approve_registration, name='startup_approve_registration'),

    # student registrations
    path('registrations/v2/students', StudentRegistrationsListView.as_view(), name='student_registrations_list'),
    path('registrations/v2/student/<int:pk>', student_registration_details, name='student_registration_details'),
    path('registrations/student/approve_registration', student_approve_registration, name='student_approve_registration'),

    # vc registrations
    path('registrations/v2/vc', VCRegistrationsListView.as_view(), name='vc_registrations_list'),
    path('registrations/v2/vc/<int:pk>', vc_registration_details, name='vc_registration_details'),
    path('registrations/vc/approve_registration', vc_approve_registration, name='vc_approve_registration'),

     # industry registrations
    path('registrations/v2/industrys', IndustryRegistrationsListView.as_view(), name='industry_registrations_list'),
    path('registrations/v2/industry/<int:pk>', industry_registration_details, name='industry_registration_details'),
    path('registrations/industry/approve_registration', industry_approve_registration, name='industry_approve_registration'),
    
    #Mentor registrations
    path('registrations/v2/mentors', MentorRegistrationsListView.as_view(), name='mentor_registrations_list'),
    path('registrations/v2/mentor/<int:pk>', mentor_registration_details, name='mentor_registration_details'),
    path('registrations/mentor/approve_registration', mentor_approve_registration, name='mentor_approve_registration'),
    
    
    

    # startup profiles
    path('profiles/v2/startups', StartUpListView.as_view(), name='startup_profiles_list'),
    path('profiles/v2/startup/<int:pk>', startup_profile_details, name='startup_profile_details'),

    # sme profiles
    path('profiles/v2/researchers', ResearcherListView.as_view(), name='researcher_profiles_list'),
    path('profiles/v2/researcher/<int:pk>', researcher_profile_details, name='researcher_profile_details'),
    

    # student profiles
    path('profiles/v2/students', StudentListView.as_view(), name='student_profiles_list'),
    path('profiles/v2/student/<int:pk>', student_profile_details, name='student_profile_details'),

    # vc profiles
    path('profiles/v2/vc', VCListView.as_view(), name='vc_profiles_list'),
    path('profiles/v2/vc/<int:pk>', vc_profile_details, name='vc_profile_details'),

    # industry profiles
    path('profiles/v2/industrys', IndustryListView.as_view(), name='industry_profiles_list'),
    path('profiles/v2/industry/<int:pk>', industry_profile_details, name='industry_profile_details'),

]