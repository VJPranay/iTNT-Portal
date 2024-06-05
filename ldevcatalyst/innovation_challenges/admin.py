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
    list_display = ('name', 'created', 'updated', 'created_by', 'updated_by')
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

class InnovationChallengeProposalTangibleBenfitsInline(admin.TabularInline):
    model = InnovationChallengeProposalTangibleBenfits

class InnovationChallengeProposalAdmin(admin.ModelAdmin):
    inlines = [
        InnovationChallengeProposalFilesInline,
        InnovationChallengeProposalExpertsInvolvedInline,
        InnovationChallengeProposalSolutionAdvantagesInline,
        InnovationChallengeProposalTangibleBenfitsInline,
    ]
    list_display = ('id', 'name', 'ip_status', 'created', 'updated', 'created_by', 'updated_by')

    # Helper function to draw text, handling long text and new pages
    def draw_text(self, p, text, x, y, line_height, page_width, page_height):
        wrapped_text = p.beginText(x, y)
        wrapped_text.setFont("Helvetica", 12)
        
        lines = text.split('\n')
        for line in lines:
            while line:
                if y < line_height:
                    p.showPage()
                    y = page_height - line_height
                    wrapped_text = p.beginText(x, y)
                    wrapped_text.setFont("Helvetica", 12)

                # Split line to fit within page width
                available_width = page_width - 2 * x
                max_chars_per_line = int(available_width // 7)  # Approximate chars that fit into the available width
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
        p.setFont("Helvetica-Bold", 14)
        p.drawString(100, page_height - 50, "Innovation Challenge Proposal Data")

        # Reset to default font
        p.setFont("Helvetica", 12)

        # Define the starting point for the rows
        y = page_height - 100
        line_height = 20

        # Get all field names of the InnovationChallengeProposal model
        fields = [field for field in InnovationChallengeProposal._meta.get_fields() if not field.is_relation and not field.many_to_many]

        for item in queryset:
            for field in fields:
                field_name = field.verbose_name.title() if field.verbose_name else field.name.title()
                field_value = getattr(item, field.name, 'N/A')

                if field.is_relation:
                    field_value = str(field_value)

                y = self.draw_text(p, f"{field_name}:", 100, y, line_height, page_width, page_height)
                y = self.draw_text(p, str(field_value), 100, y - line_height, line_height, page_width, page_height)

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