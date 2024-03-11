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

admin.site.register(InnovationChallengeProposal, InnovationChallengeProposalAdmin)
