from django.contrib import admin
from django.http import HttpResponse
from django.core.files.storage import default_storage
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from .models import RollsRoyceProposal
from django.contrib.auth.models import User
import os
import zipfile
from io import BytesIO

class RollsRoyceProposalAdmin(admin.ModelAdmin):
    list_display = ('solution_name', 'user', 'focus_area', 'team_size', 'innovation_current_stage')
    list_filter = ('focus_area', 'innovation_current_stage')
    search_fields = ('solution_name', 'user__username')
    readonly_fields = ('user',)
    fieldsets = (
        (None, {
            'fields': ('user', 'solution_name', 'focus_area', 'team_size', 'innovation_current_stage', 'patent_status')
        }),
        ('Details', {
            'fields': ('team_composition', 'solution_brief', 'solution_uniqueness', 'solution_sustainable_development_goals', 'proposed_rc_research_papers_exist', 'proposed_rc_research_papers_count', 'proposed_rc_research_papers_links', 'proposed_rc_research_papers_files', 'timeframe', 'expected_impacts_outcomes','supporting_documents'),
            'classes': ('collapse',),
        }),
    )

    def draw_text(self, p, text, x, y, line_height, page_width, page_height, bold=False, font_size=12):
        wrapped_text = p.beginText(x, y)
        font = "Helvetica-Bold" if bold else "Helvetica"
        wrapped_text.setFont(font, font_size)

        lines = text.split('\n')
        for line in lines:
            while line:
                if y < line_height:
                    p.showPage()
                    y = page_height - line_height
                    wrapped_text = p.beginText(x, y)
                    wrapped_text.setFont(font, font_size)

                available_width = page_width - 2 * x
                max_chars_per_line = int(available_width // (font_size * 0.6))
                line_split = line[:max_chars_per_line]
                line_remainder = line[max_chars_per_line:]

                wrapped_text.textLine(line_split)
                y -= line_height
                line = line_remainder

        p.drawText(wrapped_text)
        return y

    def export_as_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="RollsRoyce_Proposals.pdf"'
        p = canvas.Canvas(response, pagesize=letter)
        page_width, page_height = letter

        p.setFont("Helvetica-Bold", 16)
        p.drawString(100, page_height - 50, "RollsRoyce Proposal Data")

        p.setFont("Helvetica", 12)
        y = page_height - 100
        line_height = 20

        fields_to_display = [
            ('user', 'User'),
            ('solution_name', 'Solution Name'),
            ('focus_area', 'Focus Area'),
            ('team_size', 'Team Size'),
            ('team_composition', 'Team Composition'),
            ('solution_brief', 'Solution Brief'),
            ('solution_uniqueness', 'Solution Uniqueness'),
            ('solution_sustainable_development_goals', 'Sustainable Development Goals'),
            ('innovation_current_stage', 'Innovation Current Stage'),
            ('patent_status', 'Patent Status'),
            ('proposed_rc_research_papers_exist', 'Research Papers Exist'),
            ('proposed_rc_research_papers_count', 'Research Papers Count'),
            ('proposed_rc_research_papers_links', 'Research Papers Links'),
            ('timeframe', 'Timeframe'),
            ('expected_impacts_outcomes', 'Expected Impacts/Outcomes'),
        ]

        for obj in queryset:
            for field_path, field_display in fields_to_display:
                field_value = getattr(obj, field_path, 'N/A')
                if field_path == 'user':
                    field_value = obj.user.username if obj.user else 'N/A'
                if field_path == 'proposed_rc_research_papers_links' and field_value != 'N/A':
                    field_value = request.build_absolute_uri(field_value)

                if field_path == 'proposed_rc_research_papers_links':
                    y = self.draw_text(p, f"{field_display}:", 100, y, line_height, page_width, page_height, bold=True, font_size=14)
                    y = self.draw_text(p, str(field_value), 100, y - line_height, line_height, page_width, page_height, bold=False, font_size=12)
                    y -= line_height
                    if y < 50:
                        p.showPage()
                        y = page_height - 50
                    continue

                y = self.draw_text(p, f"{field_display}:", 100, y, line_height, page_width, page_height, bold=True, font_size=14)
                y = self.draw_text(p, str(field_value), 100, y - line_height, line_height, page_width, page_height, bold=False, font_size=12)
                y -= line_height
                if y < 50:
                    p.showPage()
                    y = page_height - 50

            y -= line_height

        p.save()
        return response

    export_as_pdf.short_description = "Export selected to PDF"

    def export_supporting_documents(self, request, queryset):
        zip_buffer = BytesIO()
        with zipfile.ZipFile(zip_buffer, 'w') as zip_file:
            for obj in queryset:
                if obj.supporting_documents:
                    file_path = obj.supporting_documents.path
                    with default_storage.open(file_path, 'rb') as f:
                        zip_file.writestr(os.path.basename(file_path), f.read())

        zip_buffer.seek(0)
        response = HttpResponse(zip_buffer, content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="Supporting_Documents.zip"'

        return response

    export_supporting_documents.short_description = "Export Supporting Documents"

    actions = [export_as_pdf, export_supporting_documents]

admin.site.register(RollsRoyceProposal, RollsRoyceProposalAdmin)
