from django.contrib import admin
from .models import (
    ChallengesCategory,
    ChallengeSubCategory,
    InnovationChallenge,
    InnovationChallengeObjectives,
    InnovationChallengeEligibilityCriteria,
    InnovationChallengeEvaluationCriteria,
    InnovationChallengeOutcomes,
    InnovationChallengeDetails,
    InnovationChallengeProposal,
    InnovationChallengeProposalBenfits,
    InnovationChallengeProposalMilestones,
    InnovationChallengeProposalTeam,
    InnovationChallengeProposalFiles,
    InnovationChallengeProposalDetails,
)

class InnovationChallengeObjectivesInline(admin.TabularInline):
    model = InnovationChallengeObjectives

class InnovationChallengeEligibilityCriteriaInline(admin.TabularInline):
    model = InnovationChallengeEligibilityCriteria

class InnovationChallengeEvaluationCriteriaInline(admin.TabularInline):
    model = InnovationChallengeEvaluationCriteria

class InnovationChallengeOutcomesInline(admin.TabularInline):
    model = InnovationChallengeOutcomes

class InnovationChallengeDetailsInline(admin.TabularInline):
    model = InnovationChallengeDetails

class InnovationChallengeProposalBenefitsInline(admin.TabularInline):
    model = InnovationChallengeProposalBenfits

class InnovationChallengeProposalMilestonesInline(admin.TabularInline):
    model = InnovationChallengeProposalMilestones

class InnovationChallengeProposalTeamInline(admin.TabularInline):
    model = InnovationChallengeProposalTeam

class InnovationChallengeProposalFilesInline(admin.TabularInline):
    model = InnovationChallengeProposalFiles

class InnovationChallengeProposalDetailsInline(admin.TabularInline):
    model = InnovationChallengeProposalDetails

@admin.register(ChallengesCategory)
class ChallengesCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(ChallengeSubCategory)
class ChallengeSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category',)

@admin.register(InnovationChallenge)
class InnovationChallengeAdmin(admin.ModelAdmin):
    inlines = [
        InnovationChallengeObjectivesInline,
        InnovationChallengeEligibilityCriteriaInline,
        InnovationChallengeEvaluationCriteriaInline,
        InnovationChallengeOutcomesInline,
    ]
    list_display = ('name', 'challenge_category', 'challenges_sub_category', 'created', 'updated', 'created_by', 'updated_by',)

@admin.register(InnovationChallengeObjectives)
class InnovationChallengeObjectivesAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'description',)

@admin.register(InnovationChallengeEligibilityCriteria)
class InnovationChallengeEligibilityCriteriaAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'description',)

@admin.register(InnovationChallengeEvaluationCriteria)
class InnovationChallengeEvaluationCriteriaAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'description',)

@admin.register(InnovationChallengeOutcomes)
class InnovationChallengeOutcomesAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'description',)

@admin.register(InnovationChallengeDetails)
class InnovationChallengeDetailsAdmin(admin.ModelAdmin):
    list_display = ('challenge', 'description', 'funding_details',)

@admin.register(InnovationChallengeProposal)
class InnovationChallengeProposalAdmin(admin.ModelAdmin):
    inlines = [
        InnovationChallengeProposalBenefitsInline,
        InnovationChallengeProposalMilestonesInline,
        InnovationChallengeProposalTeamInline,
        InnovationChallengeProposalFilesInline,
    ]
    list_display = ('challenge', 'submitted_by', 'name', 'market_domain', 'created', 'updated', 'created_by', 'updated_by', 'ip_status',)

@admin.register(InnovationChallengeProposalBenfits)
class InnovationChallengeProposalBenefitsAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'description',)

@admin.register(InnovationChallengeProposalMilestones)
class InnovationChallengeProposalMilestonesAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'description',)

@admin.register(InnovationChallengeProposalTeam)
class InnovationChallengeProposalTeamAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'name', 'mobile', 'email', 'role',)

@admin.register(InnovationChallengeProposalFiles)
class InnovationChallengeProposalFilesAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'name', 'notes', 'document',)

@admin.register(InnovationChallengeProposalDetails)
class InnovationChallengeProposalDetailsAdmin(admin.ModelAdmin):
    list_display = ('proposal', 'breif', 'value_proposition', 'solution_readiness', 'timeline',)
