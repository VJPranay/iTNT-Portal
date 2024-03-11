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
    })




@login_required
def create_challenge(request):
    if request.user.user_role in [2,3,4]:
        user_role = request.user.user_role
        if request.method == 'POST':
            challenge_form = InnovationChallengeForm(request.POST, request.FILES,user_role=user_role,user_id=request.user.id)
            details_form = InnovationChallengeDetailsForm(request.POST)
            if challenge_form.is_valid():
                challenge = challenge_form.save(commit=False)
                challenge.created_by = request.user
                challenge.save()

                            # Process InnovationChallengeDetails form
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