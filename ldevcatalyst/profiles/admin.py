from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Patent, Publication, VC, Researcher, StartUp, Student, Industry


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
    list_display = ('id','partner_name', 'firm_name', 'email', 'mobile', 'district', 'state', 'area_of_interest', 'funding_stage', 'company_website', 'linkedin_profile')

@admin.register(Researcher)
class ResearcherAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'department', 'institution', 'email', 'mobile', 'district', 'state', 'highest_qualification')

@admin.register(StartUp)
class StartUpAdmin(admin.ModelAdmin):
    list_display = ('id','company_name', 'co_founders_count', 'founder_names', 'state', 'district', 'team_size', 'email', 'mobile', 'dpiit_number', 'area_of_interest')

@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'institution', 'department', 'year_of_graduation', 'district', 'state')

@admin.register(Industry)
class IndustryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'industry', 'state', 'district', 'point_of_contact_name', 'email', 'mobile')

