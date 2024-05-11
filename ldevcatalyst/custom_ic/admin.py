from django.contrib import admin
from .models import RollsRoyceProposal

class RollsRoyceProposalAdmin(admin.ModelAdmin):
    list_display = ('solution_name', 'user', 'focus_area', 'team_size', 'innovation_current_stage', )
    list_filter = ('focus_area', 'innovation_current_stage')
    search_fields = ('solution_name', 'user__username')
    readonly_fields = ('user',)
    fieldsets = (
        (None, {
            'fields': ('user', 'solution_name', 'focus_area', 'team_size', 'innovation_current_stage', 'patent_status')
        }),
        ('Details', {
            'fields': ('team_composition', 'solution_brief', 'solution_uniqueness', 'solution_sustainable_development_goals', 'proposed_rc_research_papers_exist', 'proposed_rc_research_papers_count', 'proposed_rc_research_papers_links', 'proposed_rc_research_papers_files', 'timeframe', 'expected_impacts_outcomes', 'supporting_documents',),
            'classes': ('collapse',),
        }),
    )

admin.site.register(RollsRoyceProposal, RollsRoyceProposalAdmin)
