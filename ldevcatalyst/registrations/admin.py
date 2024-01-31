from django.contrib import admin
from .models import Patent, Publication, VC, Researcher, StartUp, Student, IndustryCategory, Industry

@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = ['number', 'title', 'inventors', 'filing_date', 'status']

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ['title', 'paper_link', 'journal']

@admin.register(VC)
class VCAdmin(admin.ModelAdmin):
    list_display = ['partner_name', 'firm_name', 'email_address', 'contact_number', 'district', 'state', 'area_of_interest', 'preferred_investment_stage']

@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'institution', 'district', 'state', 'email_id', 'mobile_number']

@admin.register(StartUp)
class StartUpAdmin(admin.ModelAdmin):
    list_display = ['name', 'co_founder_count', 'founder_names', 'state', 'district', 'team_size', 'email_address', 'mobile_number']

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['name', 'institution', 'department', 'year_of_graduation', 'district', 'state']

@admin.register(IndustryCategory)
class IndustryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ['name', 'industry', 'state', 'district', 'point_of_contact_name', 'poc_mail_id']
