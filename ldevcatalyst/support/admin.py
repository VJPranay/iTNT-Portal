from django.contrib import admin
from .models import SupportRequest

@admin.register(SupportRequest)
class SupportRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'mobile', 'account_role', 'support_category', 'created_at')
    search_fields = ('name', 'email', 'mobile', 'account_role', 'support_category', 'short_description')
    list_filter = ('account_role', 'support_category', 'created_at')
    ordering = ('-created_at',)