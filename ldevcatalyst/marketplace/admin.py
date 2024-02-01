from django.contrib import admin
from .models import Products, ProductBenfits, Services, TangibleBenfits

class ProductBenfitsInline(admin.TabularInline):
    model = ProductBenfits

class TangibleBenfitsInline(admin.TabularInline):
    model = TangibleBenfits

@admin.register(Products)
class ProductsAdmin(admin.ModelAdmin):
    inlines = [ProductBenfitsInline]
    list_display = ('start_up', 'name', 'breif', 'value_proposition', 'solution_advantage', 'product_readiness', 'implementation_time', 'ip_status')

@admin.register(ProductBenfits)
class ProductBenfitsAdmin(admin.ModelAdmin):
    list_display = ('product', 'description')

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    inlines = [TangibleBenfitsInline]
    list_display = ('start_up', 'name', 'breif', 'value_proposition', 'solution_advantage', 'service_readiness', 'implementation_time', 'ip_status')

@admin.register(TangibleBenfits)
class TangibleBenfitsAdmin(admin.ModelAdmin):
    list_display = ('product', 'description')
