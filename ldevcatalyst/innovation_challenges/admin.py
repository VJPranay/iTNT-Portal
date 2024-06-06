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

    

admin.site.register(InnovationChallengeProposal, InnovationChallengeProposalAdmin)
