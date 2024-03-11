from django import forms
from .models import InnovationChallengeProposal, InnovationChallengeProposalTangibleBenfits, \
    InnovationChallengeProposalSolutionAdvantages, InnovationChallengeProposalExpertsInvolved, \
    InnovationChallengeProposalFiles
from .models import (
    InnovationChallenge,
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
from profiles.models import User, Industry
from django import forms
from django.forms import inlineformset_factory
from .models import InnovationChallengeProposal, InnovationChallengeProposalFiles, InnovationChallengeProposalExpertsInvolved, InnovationChallengeProposalSolutionAdvantages, InnovationChallengeProposalTangibleBenfits


class InnovationChallengeForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        user_role = kwargs.pop('user_role', None)
        user_id = kwargs.pop('user_id', None)  # Get user role from kwargs
        super(InnovationChallengeForm, self).__init__(*args, **kwargs)
        if user_role == 4:  # Industry user
            industry_queryset = Industry.objects.filter(user_id=user_id)
            initial_industry = industry_queryset.first()
            self.fields['industry'].queryset = industry_queryset
            self.fields['industry'].widget = forms.HiddenInput()  # Render as hidden input
            self.fields['industry'].initial = initial_industry.pk if initial_industry else None
            user_instance = User.objects.get(id=user_id)
            self.fields['created_by'].initial = user_instance
            self.fields['created_by'].widget = forms.HiddenInput()
              # Disable the field
        elif user_role in [2,3]:  # Other users
            self.fields['industry'].queryset = Industry.objects.all()
            self.fields['created_by'].queryset = User.objects.filter(id=user_id)
            self.fields['created_by'].widget = forms.HiddenInput()
        else:
            self.fields['industry'].widget.attrs['disabled'] = 'disabled'

    class Meta:
        model = InnovationChallenge
        fields = ['industry', 'name', 'area_of_interest', 'cover_image','created_by']

class InnovationChallengeDetailsForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeDetails
        fields = ['description', 'scenario']


class InnovationTargetBeneficiariesForm(forms.ModelForm):
    class Meta:
        model = InnovationTargetBeneficiaries
        fields = ['description']

class InnovationChallengeRequirementsForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeRequirements
        fields = ['description']

class InnovationChallengeOperationalCapabilitiesForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeOperationalCapabilities
        fields = ['description']


class InnovationChallengeTangibleOutcomesForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeTangibleOutcomes
        fields = ['description']

class InnovationChallengeOtherRequrimentsForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeOtherRequriments
        fields = ['description']


class InnovationChallengeObjectivesForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeObjectives
        fields = ['description']


class InnovationChallengeEligibilityCriteriaForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeEligibilityCriteria
        fields = ['description']



class InnovationChallengeEvaluationCriteriaForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeEvaluationCriteria
        fields = ['description']



class InnovationChallengeProposalForm(forms.ModelForm):
    class Meta:
        model = InnovationChallengeProposal
        fields = ['name', 'brief', 'value_proposition', 'solution_readiness', 'implementation_time', 'ip_status','challenge']
        widgets = {'challenge': forms.HiddenInput()}

InnovationChallengeProposalFilesFormset = inlineformset_factory(
    InnovationChallengeProposal,
    InnovationChallengeProposalFiles,
    fields=['name', 'document'],
    extra=1,
    can_delete=True
)

InnovationChallengeProposalExpertsInvolvedFormset = inlineformset_factory(
    InnovationChallengeProposal,
    InnovationChallengeProposalExpertsInvolved,
    fields=['name', 'mobile', 'email', 'role'],
    extra=1,
    can_delete=True
)

InnovationChallengeProposalSolutionAdvantagesFormset = inlineformset_factory(
    InnovationChallengeProposal,
    InnovationChallengeProposalSolutionAdvantages,
    fields=['description'],
    extra=1,
    can_delete=True
)

InnovationChallengeProposalTangibleBenfitsFormset = inlineformset_factory(
    InnovationChallengeProposal,
    InnovationChallengeProposalTangibleBenfits,
    fields=['description'],
    extra=1,
    can_delete=True
)
