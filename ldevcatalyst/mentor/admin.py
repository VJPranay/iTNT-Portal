from django.contrib import admin
from .models import MentorRegistration
# Register your models here.


class MentorAdmin(admin.ModelAdmin): 
    list_display = ('id','name','mobile','email','company_name','designation','linkedin_url','profile_picture','updated_bio','certified_mentor','area_of_interest','functional_areas_of_expertise','mentoring_experience','motivation_for_mentoring','category_represent_you','mentees_journey','commitment_as_mentor','intensive_mentoring_program',
        'state','district','created','updated','registration_id')
    list_filter = ('name','id','area_of_interest')
    search_fields = ('name','mobile','email')
    
admin.site.register(MentorRegistration, MentorAdmin)