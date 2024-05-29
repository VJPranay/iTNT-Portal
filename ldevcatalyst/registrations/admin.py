from django.contrib import admin
from .models import PatentInfo, PublicationInfo, VCRegistrations, ResearcherRegistrations, StudentRegistrations, IndustryRegistrations, StartUpRegistrations, StartUpRegistrationsCoFounders
from import_export.admin import ImportExportMixin
from import_export import resources, fields
from import_export.widgets import ManyToManyWidget




@admin.register(PatentInfo)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'number', 'inventors', 'filing_date', 'status')

@admin.register(PublicationInfo)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'paper_link', 'journal')

#vc admin
class VCRegistrationsResource(resources.ModelResource):
    area_of_interest = fields.Field(
        attribute='area_of_interest',
        column_name='area_of_interest',
        widget=ManyToManyWidget(VCRegistrations, field='name', separator=' | ')
    )
    funding_stage = fields.Field(
        attribute='funding_stage',
        column_name='funding_stage',
        widget=ManyToManyWidget(VCRegistrations, field='name', separator=' | ')
    )
    class Meta:
        model = VCRegistrations
        fields = ('id','partner_name', 'firm_name', 'designation', 'email', 'mobile', 
                    'deal_size_range_min', 'deal_size_range_max', 'deal_size_range', 
                    'deal_size_range_usd', 'portfolio_size', 'district__name', 'state__name', 
                    'company_website', 'linkedin_profile', 'created', 'updated', 'area_of_interest', 'funding_stage',
                    'registration_id', 'status')
        export_order = ('id','partner_name', 'firm_name', 'designation', 'email', 'mobile', 
                    'deal_size_range_min', 'deal_size_range_max', 'deal_size_range', 
                    'deal_size_range_usd', 'portfolio_size', 'district__name', 'state__name', 
                    'company_website', 'linkedin_profile', 'created', 'updated', 'area_of_interest', 'funding_stage',
                    'registration_id', 'status')
        
        

@admin.register(VCRegistrations)
class VCAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = VCRegistrationsResource
    list_display = ('id', 'partner_name', 'firm_name', 'email', 'mobile', 'district', 'state',  'company_website', 'linkedin_profile')

#researcher admin

class ResearcherResource(resources.ModelResource):
    area_of_interest = fields.Field(
        attribute='area_of_interest',
        column_name='area_of_interest',
        widget=ManyToManyWidget(ResearcherRegistrations, field='name', separator=' | ')
    )
    patents = fields.Field(
        attribute='patents',
        column_name='patents',
        widget=ManyToManyWidget(PatentInfo, field='title', separator=' | ')
    )


    class Meta:
        model = ResearcherRegistrations
        fields =  ('id','name', 'department__name', 'institution__name', 'district__name', 'state__name', 
                    'email', 'gender', 'mobile', 'area_of_interest', 
                    'highest_qualification', 'patents','publications', 'created', 
                    'updated', 'registration_id', 'status', )
        export_order = ('id','name', 'department__name', 'institution__name', 'district__name', 'state__name', 
                    'email', 'gender', 'mobile', 'area_of_interest', 
                    'highest_qualification', 'patents','publications', 'created', 
                    'updated', 'registration_id', 'status', )


@admin.register(ResearcherRegistrations)
class ResearcherAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = ResearcherResource
    list_display = ('id','name', 'department', 'email', 'mobile', 'district', 'institution', 'status')
    raw_id_fields = ('institution',)
    list_filter = ('status','institution','area_of_interest')
    
    
    
#start up admin
class StartUpRegistrationsCoFoundersInline(admin.TabularInline):
    model = StartUpRegistrationsCoFounders
    extra = 1  # Number of extra forms to display

class StartUpRegistrationsResource(resources.ModelResource):
    class Meta:
        model = StartUpRegistrations
        fields = ('id',
        'company_name',
        'co_founder_count',
        'team_size',
        'funding_request_amount',
        'year_of_establishment',
        'dpiit_number',
        'company_description',
        'state__name',
        'district__name',
        'area_of_interest__name',
        'preferred_investment_stage',
        'fund_raised',
        'primary_business_model',
        'incubator_associated',
        'client_customer_size',
        'reveune_stage',
        'development_stage',
        'development_stage_document',
        'company_website',
        'company_linkedin',
        'video_link',
        'pitch_deck',
        'company_logo',
        'created',
        'updated',
        'registration_id',
        'status',
        'data_source',)

@admin.register(StartUpRegistrations)
class StartUpRegistrationsAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = StartUpRegistrationsResource
    inlines = [StartUpRegistrationsCoFoundersInline]
    list_display = [
        'id',
        'company_name',
        'co_founders_count',
        'team_size',
        'state',
        'district',
        'funding_request_amount',
        'dpiit_number',
        'area_of_interest',
    ]
    

#student admin
class StudentRegistrationsResource(resources.ModelResource):
    area_of_interest = fields.Field(
        attribute='area_of_interest',
        column_name='area_of_interest',
        widget=ManyToManyWidget(StudentRegistrations, field='name', separator=' | ')
    )

    class Meta:
        model = StudentRegistrations
        fields =  ('id','name', 'institution__name', 'area_of_interest', 'department__name', 
                    'year_of_graduation', 'email', 'district__name', 'state__name', 
                    'project_idea', 'created', 'updated', 'registration_id', 'status')
        export_order = ('id','name', 'institution__name', 'area_of_interest', 'department__name', 
                    'year_of_graduation', 'email', 'district__name', 'state__name', 
                    'project_idea', 'created', 'updated', 'registration_id', 'status')
        
        
@admin.register(StudentRegistrations)
class StudentAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = StudentRegistrationsResource
    list_display = ('id','name', 'institution', 'department', 'year_of_graduation', 'district', 'state','highest_qualification','paper_published')



#industy admin
class IndustryRegistrationsResource(resources.ModelResource):
    area_of_interest = fields.Field(
        attribute='area_of_interest',
        column_name='area_of_interest',
        widget=ManyToManyWidget(IndustryRegistrations, field='name', separator=' | ')
    )

    class Meta:
        model = IndustryRegistrations
        fields = ('id','name', 'industry__name', 'state__name', 'district__name', 'point_of_contact_name', 
                    'email', 'mobile', 'area_of_interest', 'created', 'updated', 
                    'registration_id', 'status')
        export_order = ('id','name', 'industry__name', 'state__name', 'district__name', 'point_of_contact_name', 
                    'email', 'mobile', 'area_of_interest', 'created', 'updated', 
                    'registration_id', 'status')
        
@admin.register(IndustryRegistrations)
class IndustryAdmin(ImportExportMixin,admin.ModelAdmin):
    resource_class = IndustryRegistrationsResource
    list_display = ('id','name', 'industry', 'state', 'district', 'point_of_contact_name', 'email', 'mobile')
