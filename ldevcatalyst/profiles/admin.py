from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patent, Publication, VC, Researcher, StartUp, Student, Industry,Mentor


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'user_role')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'password1', 'password2', 'email', 'user_role'),
        }),
    )
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'user_role')
    search_fields = ('username', 'email', 'first_name', 'last_name')
    ordering = ('username',)

admin.site.register(User, UserAdmin)

@admin.register(Patent)
class PatentAdmin(admin.ModelAdmin):
    list_display = ('title', 'number', 'inventors', 'filing_date', 'status')

@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    list_display = ('title', 'paper_link', 'journal')

@admin.register(VC)
class VCAdmin(admin.ModelAdmin):
    list_display = ('id','partner_name', 'firm_name', 'email', 'mobile', 'district', 'state', 'company_website', 'linkedin_profile')

@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('id','user','name', 'department', 'institution', 'email', 'mobile', 'district', 'state', 'highest_qualification')

@admin.register(StartUp)
class StartUpAdmin(admin.ModelAdmin):
    list_display = ('id','company_name', 'co_founders_count', 'founder_names', 'state', 'district', 'team_size', 'email', 'mobile', 'dpiit_number', 'area_of_interest')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'institution', 'department', 'year_of_graduation', 'district', 'state')

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'industry', 'state', 'district', 'point_of_contact_name', 'email', 'mobile')


@admin.register(Mentor)
class MentorAdmin(admin.ModelAdmin):
    list_display = (
        
        'id','user', 'name', 'mobile', 'address', 'email', 'gender', 'profile_picture',
        'company_name', 'designation', 'linkedin_url', 'updated_bio', 'certified_mentor',
        'reason','area_of_interest', 'functional_areas_of_expertise', 'mentoring_experience',
        'motivation_for_mentoring', 'category_represent_you', 'mentees_journey','commitment_as_mentor','intensive_mentoring_program',
        'state','district','created', 'updated', 'approved',  
    )

