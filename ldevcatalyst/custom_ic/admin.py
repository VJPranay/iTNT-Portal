from django.contrib import admin
from django.http import HttpResponse
from django.core.files.storage import default_storage
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Frame
from .models import RollsRoyceProposal
from io import BytesIO
import zipfile
import os
from django.conf import settings

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

    def _register_fonts(self):
        font_dir = os.path.join(settings.BASE_DIR, 'custom_ic/fonts')
        pdfmetrics.registerFont(TTFont('NotoSans-Regular', os.path.join(font_dir, 'NotoSans-Regular.ttf')))
        pdfmetrics.registerFont(TTFont('NotoSans-Bold', os.path.join(font_dir, 'NotoSans-Bold.ttf')))
        pdfmetrics.registerFont(TTFont('NotoSans-Italic', os.path.join(font_dir, 'NotoSans-Italic.ttf')))

    def _add_background_and_images(self, canvas_obj, doc):
        width, height = doc.pagesize
        files_dir = os.path.join(settings.BASE_DIR, 'custom_ic/files')

        # Calculate the aspect ratio matching the page size without stretching the image
        background_path = os.path.join(files_dir, 'background.jpg')
        img = canvas.ImageReader(background_path)
        img_width, img_height = img.getSize()
        aspect = img_width / float(img_height)

        if aspect > 1:
            # Wide image
            img_width = width
            img_height = width / aspect
        else:
            # Tall image
            img_height = height
            img_width = height * aspect

        # canvas_obj.drawImage(background_path, (width - img_width) / 2, (height - img_height) / 2, width=img_width, height=img_height, preserveAspectRatio=True)

        # # Add the iTNT logo to the top right without black strip and jigsaw logo
        # canvas_obj.drawImage(os.path.join(files_dir, 'iTNT.png'), width-2*inch, height-1*inch, width=1.5*inch, height=1.5*inch, mask='auto')

    def export_as_pdf(self, request, queryset):
        self._register_fonts()
        buffer = BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        styles = getSampleStyleSheet()
        styles.add(ParagraphStyle(name='CustomTitle', fontName='NotoSans-Bold', fontSize=24, leading=30, textColor=colors.black, spaceAfter=20))
        styles.add(ParagraphStyle(name='CustomHeading', fontName='NotoSans-Bold', fontSize=16, leading=20, textColor=colors.orange, spaceAfter=10))
        styles.add(ParagraphStyle(name='CustomSubHeading', fontName='NotoSans-Italic', fontSize=14, leading=18, textColor=colors.yellow, spaceAfter=10))
        styles.add(ParagraphStyle(name='CustomBody', fontName='NotoSans-Regular', fontSize=12, leading=15, spaceAfter=10))

        elements = [Paragraph("RollsRoyce Proposal Data", styles['CustomTitle'])]
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
                elements.append(Paragraph(f"<b>{field_display}:</b>", styles['CustomHeading']))
                elements.append(Paragraph(str(field_value), styles['CustomBody']))
            elements.append(Spacer(1, 0.2 * inch))

        def on_first_page(canvas_obj, doc):
            self._add_background_and_images(canvas_obj, doc)

        doc.build(elements, onFirstPage=on_first_page)
        pdf = buffer.getvalue()
        buffer.close()
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="RollsRoyce_Proposals.pdf"'

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