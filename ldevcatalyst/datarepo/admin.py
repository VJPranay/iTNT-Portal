from django.contrib import admin
from .models import AreaOfInterest, PreferredInvestmentStage, Department, Institution, District, State, IndustryCategory

# Register your models here.

@admin.register(AreaOfInterest)
class AreaOfInterestAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(PreferredInvestmentStage)
class PreferredInvestmentStageAdmin(admin.ModelAdmin):
    list_display = ['name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['name','district','district__state']
    search_fields = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(IndustryCategory)
class IndustryCategoryAdmin(admin.ModelAdmin):
    list_display = ['name']