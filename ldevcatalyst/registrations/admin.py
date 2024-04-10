from django.contrib import admin
from .models import PatentInfo, PublicationInfo, VCRegistrations, ResearcherRegistrations, StudentRegistrations, IndustryRegistrations, StartUpRegistrations, StartUpRegistrationsCoFounders
from import_export.admin import ImportExportMixin
from import_export import resources
class ResearcherResource(resources.ModelResource):
    class Meta:
        model = ResearcherRegistrations
        fields = ('name', 'department__name', 'email', 'mobile', 'district__name', 'institution__name', 'status')


@admin.register(PatentInfo)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'inventors', 'filing_date', 'status')

@admin.register(PublicationInfo)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'paper_link', 'journal')

@admin.register(VCRegistrations)
class VCAdmin(admin.ModelAdmin):
    list_display = ('partner_name', 'firm_name', 'email', 'mobile', 'district', 'state',  'company_website', 'linkedin_profile')

@admin.register(ResearcherRegistrations)
class ResearcherAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = ResearcherResource
    list_display = ('name', 'department', 'email', 'mobile', 'district', 'institution', 'status')
    raw_id_fields = ('institution',)
    list_filter = ('status','institution','area_of_interest')

class StartUpRegistrationsCoFoundersInline(admin.TabularInline):
    model = StartUpRegistrationsCoFounders
    extra = 1  # Number of extra forms to display

@admin.register(StartUpRegistrations)
class StartUpRegistrationsAdmin(admin.ModelAdmin):
    inlines = [StartUpRegistrationsCoFoundersInline]
    list_display = [
        'name',
        'co_founder_count',
        'founder_names',
        'state',
        'district',
        'team_size',
        'email',
        'mobile',
        'website',
        'dpiit_number',
        'area_of_interest',
        'description',
        'market_size',
        'required_amount',
        'founding_year',
        'founding_experience',
        'reveune_stage',
        'primary_business_model',
        'fund_raised',
        'fund_raised_value',
        'incubator',
        'customer_size',
        'product_development_stage',
        'funding_stage',
        'status',
        'created',
        'updated',
        'registration_id',
        'short_video',
        'company_linkedin',
        'video_link',
        'pitch_deck',
        'product_development_stage_document',
        'company_logo',
    ]
    

@admin.register(StudentRegistrations)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'institution', 'department', 'year_of_graduation', 'district', 'state')

@admin.register(IndustryRegistrations)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('name', 'industry', 'state', 'district', 'point_of_contact_name', 'email', 'mobile')
