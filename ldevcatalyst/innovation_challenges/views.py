from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .forms import (
    InnovationChallengeForm, 
    InnovationTargetBeneficiariesForm,
    InnovationChallengeRequirementsForm,
    InnovationChallengeOperationalCapabilitiesForm,
    InnovationChallengeTangibleOutcomesForm,
    InnovationChallengeOtherRequrimentsForm,
    InnovationChallengeObjectivesForm,
    InnovationChallengeEligibilityCriteriaForm,
    InnovationChallengeEvaluationCriteriaForm,
    InnovationChallengeDetailsForm
)
from .models import (
    InnovationChallenge, 
    InnovationTargetBeneficiaries,
    InnovationChallengeRequirements,
    InnovationChallengeOperationalCapabilities,
    InnovationChallengeTangibleOutcomes,
    InnovationChallengeOtherRequriments,
    InnovationChallengeObjectives,
    InnovationChallengeEligibilityCriteria,
    InnovationChallengeEvaluationCriteria,
    InnovationChallengeDetails
)
from .forms import InnovationChallengeProposalForm, InnovationChallengeProposalFilesFormset, InnovationChallengeProposalExpertsInvolvedFormset, InnovationChallengeProposalSolutionAdvantagesFormset, InnovationChallengeProposalTangibleBenfitsFormset
from .models import InnovationChallengeProposal,InnovationChallengeProposalFiles, InnovationChallengeProposalExpertsInvolved, InnovationChallengeProposalSolutionAdvantages, InnovationChallengeProposalTangibleBenfits
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages




@login_required
def innovation_challenges(request,challenge_status=None):
    if request.user.user_role in [2,3,4,5,6]:
        if challenge_status is not None:
            innovation_challenges_q = InnovationChallenge.objects.filter(status=challenge_status).order_by('-id')
        else:
            innovation_challenges_q = InnovationChallenge.objects.all().order_by('-id')
        innovation_challenges_list = []
        for x in innovation_challenges_q:
            temp = {
                'challenge_id' : x.id,
                'name':x.name,
                'industry' : x.industry,
                'created' : x.created,
            }
            innovation_challenges_list.append(temp)
        return render(request, 'dashboard/ic/list.html',context={'innovation_challenges':innovation_challenges_list})
    else:
        return render(request, 'dashboard/dashboard.html')
    

@login_required
def innovation_challenge_detail(request, challenge_id):
    # Fetch the Innovation Challenge object
    challenge = InnovationChallenge.objects.get(pk=challenge_id)

    # Fetch the Innovation Challenge Details object
    challenge_details = InnovationChallengeDetails.objects.get(challenge=challenge)

    # Fetch all records for InnovationTargetBeneficiaries
    target_beneficiaries = InnovationTargetBeneficiaries.objects.filter(challenge=challenge)

    # Fetch all records for InnovationChallengeRequirements
    requirements = InnovationChallengeRequirements.objects.filter(challenge=challenge)

    # Fetch all records for InnovationChallengeOperationalCapabilities
    operational_capabilities = InnovationChallengeOperationalCapabilities.objects.filter(challenge=challenge)

    # Fetch all records for InnovationChallengeTangibleOutcomes
    tangible_outcomes = InnovationChallengeTangibleOutcomes.objects.filter(challenge=challenge)

    # Fetch all records for InnovationChallengeOtherRequriments
    other_requirements = InnovationChallengeOtherRequriments.objects.filter(challenge=challenge)

    # Fetch all records for InnovationChallengeObjectives
    objectives = InnovationChallengeObjectives.objects.filter(challenge=challenge)

    # Fetch all records for InnovationChallengeEligibilityCriteria
    eligibility_criteria = InnovationChallengeEligibilityCriteria.objects.filter(challenge=challenge)

    # Fetch all records for InnovationChallengeEvaluationCriteria
    evaluation_criteria = InnovationChallengeEvaluationCriteria.objects.filter(challenge=challenge)

    # proposals 
    proposals = InnovationChallengeProposal.objects.filter(challenge=challenge)
    proposals_count = proposals.count()

    return render(request, 'dashboard/ic/challenge_details.html', {
        'challenge': challenge,
        'challenge_details': challenge_details,
        'target_beneficiaries': target_beneficiaries,
        'requirements': requirements,
        'operational_capabilities': operational_capabilities,
        'tangible_outcomes': tangible_outcomes,
        'other_requirements': other_requirements,
        'objectives': objectives,
        'eligibility_criteria': eligibility_criteria,
        'evaluation_criteria': evaluation_criteria,
        'proposals': proposals
    })

@login_required
def approve_challenge(request, challenge_id):
    if request.user.user_role not in [2, 3]:
        return render(request, 'dashboard/dashboard.html')
    
    try:
        challenge = InnovationChallenge.objects.get(id=challenge_id)
    except InnovationChallenge.DoesNotExist:
        messages.error(request, 'Challenge not found.')
        return redirect('dashboard')  
    
    if challenge.status == 'approved':
        messages.warning(request, 'This challenge is already approved.')
        return redirect('dashboard')  
    
    challenge.status = 'active'
    challenge.save()
    
    messages.success(request, 'Challenge published successfully.')
    
    return redirect('innovation_challenge_detail', challenge_id=challenge.id)


@login_required
def approve_proposal(request, proposal_id):
    if request.user.user_role not in [2, 3]:
        return render(request, 'dashboard/dashboard.html')
    
    proposal = get_object_or_404(InnovationChallengeProposal, id=proposal_id)
    
    if proposal.status == 'approved':
        messages.warning(request, 'This proposal is already approved.')
        return redirect('proposal_detail', proposal_id=proposal.id)
    
    proposal.status = 'approved'
    proposal.save()
    
    messages.success(request, 'Proposal approved successfully.')
    
    return redirect('proposal_detail', proposal_id=proposal.id)





@login_required
def create_challenge(request):
    if request.user.user_role in [2,3,4]:
        user_role = request.user.user_role
        if request.method == 'POST':
            challenge_form = InnovationChallengeForm(request.POST, request.FILES)
            details_form = InnovationChallengeDetailsForm(request.POST)
            if challenge_form.is_valid():
                challenge = challenge_form.save(commit=False)
                challenge.status = 'submitted'
                challenge.created_by = request.user
                challenge.save()

                detail = details_form.save(commit=False)
                detail.challenge = challenge
                detail.save()

                # Process InnovationTargetBeneficiaries forms
                for key, value in request.POST.items():
                    if key.startswith('beneficiaries-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationTargetBeneficiaries.objects.create(challenge=challenge, description=description)
                
                # Process InnovationChallengeRequirements forms
                for key, value in request.POST.items():
                    if key.startswith('requirements-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationChallengeRequirements.objects.create(challenge=challenge, description=description)

                # Process InnovationChallengeOperationalCapabilities forms
                for key, value in request.POST.items():
                    if key.startswith('capabilities-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationChallengeOperationalCapabilities.objects.create(challenge=challenge, description=description)

                # Process InnovationChallengeTangibleOutcomes forms
                for key, value in request.POST.items():
                    if key.startswith('outcomes-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationChallengeTangibleOutcomes.objects.create(challenge=challenge, description=description)

                # Process InnovationChallengeOtherRequriments forms
                for key, value in request.POST.items():
                    if key.startswith('otherrequirements-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationChallengeOtherRequriments.objects.create(challenge=challenge, description=description)

                # Process InnovationChallengeObjectives forms
                for key, value in request.POST.items():
                    if key.startswith('objectives-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationChallengeObjectives.objects.create(challenge=challenge, description=description)

                # Process InnovationChallengeEligibilityCriteria forms
                for key, value in request.POST.items():
                    if key.startswith('eligibilitycriteria-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationChallengeEligibilityCriteria.objects.create(challenge=challenge, description=description)

                # Process InnovationChallengeEvaluationCriteria forms
                for key, value in request.POST.items():
                    if key.startswith('evaluationcriteria-'):
                        prefix, _, field_name = key.rsplit('-', 2)
                        if field_name == 'description':
                            description = value
                            InnovationChallengeEvaluationCriteria.objects.create(challenge=challenge, description=description)
                return render(request, 'dashboard/ic/list.html',{})  # Redirect to success page
        else:
            challenge_form = InnovationChallengeForm(user_role=user_role,user_id=request.user.id)
            details_form = InnovationChallengeDetailsForm()
        return render(request, 'dashboard/ic/create_challenge.html', {'challenge_form': challenge_form, 'details_form': details_form})
    else:
        return redirect('dashboard_index')



@login_required
def submit_proposal(request,challenge_id):
    user_role = request.user.user_role
    challenge = get_object_or_404(InnovationChallenge, pk=challenge_id)
    if request.method == 'POST':
        proposal_form = InnovationChallengeProposalForm(request.POST)
        files_formset = InnovationChallengeProposalFilesFormset(request.POST, request.FILES, prefix='files')
        experts_formset = InnovationChallengeProposalExpertsInvolvedFormset(request.POST, prefix='experts')
        solution_advantages_formset = InnovationChallengeProposalSolutionAdvantagesFormset(request.POST, prefix='advantages')
        tangible_benefits_formset = InnovationChallengeProposalTangibleBenfitsFormset(request.POST, prefix='benefits')
        if proposal_form.is_valid() and files_formset.is_valid() and experts_formset.is_valid() and solution_advantages_formset.is_valid() and tangible_benefits_formset.is_valid():
            proposal = proposal_form.save(commit=False)
            proposal.submitted_by = request.user
            proposal.challenge = challenge
            proposal.save()
            files_formset.instance = proposal
            files_formset.save()
            experts_formset.instance = proposal
            experts_formset.save()
            solution_advantages_formset.instance = proposal
            solution_advantages_formset.save()
            tangible_benefits_formset.instance = proposal
            tangible_benefits_formset.save()
            return redirect('innovation_challenge_detail', challenge_id=challenge.id)
    else:
        proposal_form = InnovationChallengeProposalForm(initial={'challenge': challenge})
        files_formset = InnovationChallengeProposalFilesFormset(prefix='files')
        experts_formset = InnovationChallengeProposalExpertsInvolvedFormset(prefix='experts')
        solution_advantages_formset = InnovationChallengeProposalSolutionAdvantagesFormset(prefix='advantages')
        tangible_benefits_formset = InnovationChallengeProposalTangibleBenfitsFormset(prefix='benefits')
    return render(request, 'dashboard/ic/submit_proposal.html', {
        'proposal_form': proposal_form,
        'files_formset': files_formset,
        'experts_formset': experts_formset,
        'advantages_formset': solution_advantages_formset,
        'benefits_formset': tangible_benefits_formset
    })


@login_required
def proposal_detail(request, proposal_id):
    proposal = get_object_or_404(InnovationChallengeProposal, pk=proposal_id)
    tangible_benefits = proposal.innovationchallengeproposaltangiblebenfits_set.all()
    solution_advantages = proposal.innovationchallengeproposalsolutionadvantages_set.all()
    experts_involved = proposal.innovationchallengeproposalexpertsinvolved_set.all()
    proposal_files = proposal.innovationchallengeproposalfiles_set.all()

    return render(request, 'dashboard/ic/proposal_details.html', {
        'proposal': proposal,
        'tangible_benefits': tangible_benefits,
        'solution_advantages': solution_advantages,
        'experts_involved': experts_involved,
        'proposal_files': proposal_files,
    })