from django.contrib import admin
from .models import PatentInfo, PublicationInfo, VCRegistrations, ResearcherRegistrations, StudentRegistrations, IndustryRegistrations, StartUpRegistrations, StartUpRegistrationsCoFounders
from import_export.admin import ImportExportMixin
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget



@admin.register(PatentInfo)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'inventors', 'filing_date', 'status')

@admin.register(PublicationInfo)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'paper_link', 'journal')

#vc admin
class VCRegistrationsResource(resources.ModelResource):
    class Meta:
        model = VCRegistrations
        fields = ('partner_name', 'firm_name', 'designation', 'email', 'mobile', 
                    'deal_size_range_min', 'deal_size_range_max', 'deal_size_range', 
                    'deal_size_range_usd', 'portfolio_size', 'district__name', 'state__name', 
                    'company_website', 'linkedin_profile', 'created', 'updated', 
                    'registration_id', 'status')


@admin.register(VCRegistrations)
class VCAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = VCRegistrationsResource
    list_display = ('partner_name', 'firm_name', 'email', 'mobile', 'district', 'state',  'company_website', 'linkedin_profile')

#researcher admin

class ResearcherResource(resources.ModelResource):
    class Meta:
        model = ResearcherRegistrations
        fields =  ('name', 'department__name', 'institution__name', 'district__name', 'state__name', 
                    'email', 'gender', 'mobile', 'area_of_interest__name', 
                    'highest_qualification', 'publications', 'created', 
                    'updated', 'registration_id', 'status', )

@admin.register(ResearcherRegistrations)
class ResearcherAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = ResearcherResource
    list_display = ('name', 'department', 'email', 'mobile', 'district', 'institution', 'status')
    raw_id_fields = ('institution',)
    list_filter = ('status','institution','area_of_interest')
    
    
    
#start up admin
class StartUpRegistrationsCoFoundersInline(admin.TabularInline):
    model = StartUpRegistrationsCoFounders
    extra = 1  # Number of extra forms to display

class StartUpRegistrationsResource(resources.ModelResource):
    class Meta:
        model = StartUpRegistrations
        fields = ( 'name',
        'co_founder_count',
        'founder_names',
        'state__name',
        'district__name',
        'team_size',
        'email',
        'mobile',
        'website',
        'dpiit_number',
        'area_of_interest__name',
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
        'company_logo')

@admin.register(StartUpRegistrations)
class StartUpRegistrationsAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = StartUpRegistrationsResource
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
    

#student admin
class StudentRegistrationsResource(resources.ModelResource):
    class Meta:
        model = StudentRegistrations
        fields =  ('name', 'institution__name', 'area_of_interest__name', 'department__name', 
                    'year_of_graduation', 'email', 'district__name', 'state__name', 
                    'project_idea', 'created', 'updated', 'registration_id', 'status')
@admin.register(StudentRegistrations)
class StudentAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = StudentRegistrationsResource
    list_display = ('name', 'institution', 'department', 'year_of_graduation', 'district', 'state')



#industy admin
class IndustryRegistrationsResource(resources.ModelResource):
    area_of_interest = fields.Field(
        attribute='area_of_interest',
        widget=ManyToManyWidget(IndustryRegistrations, field='name', separator=',')
    )

    class Meta:
        model = IndustryRegistrations
        fields = ('name', 'industry__name', 'state__name', 'district__name', 'point_of_contact_name', 
                    'email', 'mobile', 'area_of_interest', 'created', 'updated', 
                    'registration_id', 'status')
@admin.register(IndustryRegistrations)
class IndustryAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = IndustryRegistrationsResource
    list_display = ('name', 'industry', 'state', 'district', 'point_of_contact_name', 'email', 'mobile')
