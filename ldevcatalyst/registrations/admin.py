from django.contrib import admin
from .models import PatentInfo, PublicationInfo, VCRegistrations, ResearcherRegistrations, StartUpRegistrations, StudentRegistrations, IndustryRegistrations

@admin.register(PatentInfo)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'inventors', 'filing_date', 'status')

@admin.register(PublicationInfo)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'paper_link', 'journal')

@admin.register(VCRegistrations)
class VCAdmin(admin.ModelAdmin):
    list_display = ('partner_name', 'firm_name', 'email', 'mobile', 'district', 'state', 'area_of_interest', 'funding_stage', 'company_website', 'linkedin_profile')

@admin.register(ResearcherRegistrations)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('name', 'department', 'institution', 'email', 'mobile', 'district', 'state', 'highest_qualification')

@admin.register(StartUpRegistrations)
class StartUpAdmin(admin.ModelAdmin):
    list_display = ('name', 'co_founder_count', 'founder_names', 'state', 'district', 'team_size', 'email', 'mobile', 'website', 'dpiit_number', 'area_of_interest', 'funding_stage')

@admin.register(StudentRegistrations)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'department', 'year_of_graduation', 'district', 'state')

@admin.register(IndustryRegistrations)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'state', 'district', 'point_of_contact_name', 'email', 'mobile')
