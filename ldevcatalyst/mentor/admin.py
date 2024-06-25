from django.contrib import admin
from import_export import resources
from import_export.admin import ImportExportMixin
from .models import MentorRegistration, State, District

class MentorRegistrationsResource(resources.ModelResource):
    class Meta:
        model = MentorRegistration
        fields = (
            'id', 'name', 'mobile', 'email', 'company_name', 'designation', 
            'linkedin_url', 'profile_picture', 'updated_bio', 'certified_mentor', 
            'area_of_interest__name', 'functional_areas_of_expertise', 'mentoring_experience', 
            'motivation_for_mentoring', 'category_represent_you', 'mentees_journey', 
            'commitment_as_mentor', 'intensive_mentoring_program', 'state__name', 'district__name', 
            'created', 'updated', 'registration_id'
        )
        export_order = (
            'id', 'name', 'mobile', 'email', 'company_name', 'designation', 
            'linkedin_url', 'profile_picture', 'updated_bio', 'certified_mentor', 
            'area_of_interest__name', 'functional_areas_of_expertise', 'mentoring_experience', 
            'motivation_for_mentoring', 'category_represent_you', 'mentees_journey', 
            'commitment_as_mentor', 'intensive_mentoring_program', 'state__name', 'district__name', 
            'created', 'updated', 'registration_id'
        )
        
@admin.register(MentorRegistration)
class MentorAdmin(ImportExportMixin, admin.ModelAdmin):
    resource_class = MentorRegistrationsResource
    list_display = (
        'id', 'name', 'mobile', 'email', 'company_name', 'designation', 
        'linkedin_url', 'profile_picture', 'updated_bio', 'certified_mentor',
        'reason', 
        'area_of_interest', 'functional_areas_of_expertise', 'mentoring_experience', 
        'motivation_for_mentoring', 'category_represent_you', 'mentees_journey', 
        'commitment_as_mentor', 'intensive_mentoring_program', 'state', 'district', 
        'created', 'updated', 'registration_id'
    )
