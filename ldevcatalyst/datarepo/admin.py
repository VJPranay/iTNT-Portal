from django.contrib import admin
from .models import AreaOfInterest, PreferredInvestmentStage, Department, Institution, District, State, IndustryCategory,RevenueStage,ProductDevelopmentStage,PrimaryBusinessModel,FundRaised

# Register your models here.

@admin.register(AreaOfInterest)
class AreaOfInterestAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(PreferredInvestmentStage)
class PreferredInvestmentStageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(Institution)
class InstitutionAdmin(admin.ModelAdmin):
    list_display = ['id', 'name','district']
    search_fields = ['name']

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    search_fields = ['name']

@admin.register(State)
class StateAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(IndustryCategory)
class IndustryCategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(RevenueStage)
class RevenueStageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(ProductDevelopmentStage)
class ProductDevelopmentStageAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


@admin.register(PrimaryBusinessModel)
class PrimaryBusinessModelAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(FundRaised)
class FundRaisedAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']