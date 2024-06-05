from django.contrib import admin
from .models import (InnovationChallenge,
                     InnovationChallengeDetails,
                     InnovationTargetBeneficiaries,
                     InnovationChallengeRequirements,
                     InnovationChallengeOperationalCapabilities,
                     InnovationChallengeTangibleOutcomes,
                     InnovationChallengeOtherRequriments,
                     InnovationChallengeObjectives,
                     InnovationChallengeEligibilityCriteria,
                     InnovationChallengeEvaluationCriteria
                     )
from .models import InnovationChallengeProposal, InnovationChallengeProposalFiles, InnovationChallengeProposalExpertsInvolved, InnovationChallengeProposalSolutionAdvantages, InnovationChallengeProposalTangibleBenfits
from import_export.admin import ImportExportMixin
from django.http import HttpResponse
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors



class InnovationChallengeDetailsInline(admin.StackedInline):
    model = InnovationChallengeDetails
    extra = 1


class InnovationTargetBeneficiariesInline(admin.StackedInline):
    model = InnovationTargetBeneficiaries
    extra = 1

class InnovationChallengeRequirementsInline(admin.StackedInline):
    model = InnovationChallengeRequirements
    extra = 1

class InnovationChallengeOperationalCapabilitiesInline(admin.StackedInline):
    model = InnovationChallengeOperationalCapabilities
    extra = 1

class InnovationChallengeTangibleOutcomesInline(admin.StackedInline):
    model = InnovationChallengeTangibleOutcomes
    extra = 1

class InnovationChallengeOtherRequrimentsInline(admin.StackedInline):
    model = InnovationChallengeOtherRequriments
    extra = 1

class InnovationChallengeObjectivesInline(admin.StackedInline):
    model = InnovationChallengeObjectives
    extra = 1

class InnovationChallengeEligibilityCriteriaInline(admin.StackedInline):
    model = InnovationChallengeEligibilityCriteria
    extra = 1

class InnovationChallengeEvaluationCriteriaInline(admin.StackedInline):
    model = InnovationChallengeEvaluationCriteria
    extra = 1





@admin.register(InnovationChallenge)
class InnovationChallengeAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'created', 'updated', 'created_by', 'updated_by')
    search_fields = ('name', 'created_by__username', 'updated_by__username')
    list_filter = ('created', 'updated')
    readonly_fields = ('created', 'updated')
    inlines = [
        InnovationChallengeDetailsInline, 
        InnovationTargetBeneficiariesInline,
        InnovationChallengeRequirementsInline,
        InnovationChallengeOperationalCapabilitiesInline,
        InnovationChallengeTangibleOutcomesInline,
        InnovationChallengeOtherRequrimentsInline,
        InnovationChallengeObjectivesInline,
        InnovationChallengeEligibilityCriteriaInline,
        InnovationChallengeEvaluationCriteriaInline
        ]


class InnovationChallengeProposalFilesInline(admin.TabularInline):
    model = InnovationChallengeProposalFiles

class InnovationChallengeProposalExpertsInvolvedInline(admin.TabularInline):
    model = InnovationChallengeProposalExpertsInvolved

class InnovationChallengeProposalSolutionAdvantagesInline(admin.TabularInline):
    model = InnovationChallengeProposalSolutionAdvantages
    
    def __str__(self):
        return self.model

class InnovationChallengeProposalTangibleBenfitsInline(admin.TabularInline):
    model = InnovationChallengeProposalTangibleBenfits
    
    def __str__(self):
        return self.model

class InnovationChallengeProposalAdmin(admin.ModelAdmin):
    inlines = [
        InnovationChallengeProposalFilesInline,
        InnovationChallengeProposalExpertsInvolvedInline,
        InnovationChallengeProposalSolutionAdvantagesInline,
        InnovationChallengeProposalTangibleBenfitsInline,
    ]
    list_display = ('id', 'name', 'ip_status', 'created', 'updated', 'created_by', 'updated_by')

    # Helper function to draw text, handling long text and new pages
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

                # Split line to fit within page width
                available_width = page_width - 1 * x
                max_chars_per_line = int(available_width // (font_size * 0.6))  # Approximate chars that fit into the available width
                line_split = line[:max_chars_per_line]
                line_remainder = line[max_chars_per_line:]

                wrapped_text.textLine(line_split)
                y -= line_height
                line = line_remainder

        p.drawText(wrapped_text)
        return y
    def export_as_pdf(self, request, queryset):
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="Innovation Challenge Proposal.pdf"'
        p = canvas.Canvas(response, pagesize=letter)
        page_width, page_height = letter

        # Add a bold title
        p.setFont("Helvetica-Bold",16)
        p.drawString(100, page_height - 50, "Innovation Challenge Proposal Data")

        # Reset to default font
        p.setFont("Helvetica", 12)

        # Define the starting point for the rows
        y = page_height - 100
        line_height = 20

        # Define the fields to display manually
        fields_to_display = [
            ('id', 'Proposal ID'),
            ('name', 'Name'),
            ('submitted_by', 'Submitted By'),
            ('challenge_id', 'Challenge ID'),
            ('challenge__name', 'Challenge Name'),
            ('challenge__industry_id', 'Industry ID'),
            ('challenge__industry__name', 'Industry Name'),
            ('challenge__area_of_interest_id', 'Area of Interest ID'),
            ('challenge__area_of_interest__name', 'Area of Interest Name'),
            ('brief', 'Brief'),
            ('value_proposition', 'Value Proposition'),
            ('solution_readiness', 'Solution Readiness'),
            ('implementation_time', 'Implementation Time'),
            ('ip_status', 'IP Status'),
            ('created', 'Created'),
            ('updated', 'Updated'),
            ('created_by', 'Created By'),
            ('updated_by', 'Updated By'),
        ]

        for obj in queryset:
            for field_path, field_display in fields_to_display:
                field_parts = field_path.split('__')
                field_value = obj
                for item in field_parts:
                    field_value = getattr(field_value, item, 'N/A')
                    if field_value == 'N/A':
                        break

                y = self.draw_text(p, f"{field_display}:", 100, y, line_height, page_width, page_height, bold=True, font_size=14)
                y = self.draw_text(p, str(field_value), 100, y - line_height, line_height, page_width, page_height, bold=False, font_size=12)

                # Add extra space between fields
                y -= line_height

                # Check if we need to add a new page
                if y < 50:
                    p.showPage()
                    y = page_height - 50

            # Add a blank line between records
            y -= line_height

        p.save()
        return response

    export_as_pdf.short_description = "Export selected to PDF"

    # Add the custom action to the admin actions
    actions = [export_as_pdf]

admin.site.register(InnovationChallengeProposal, InnovationChallengeProposalAdmin)
