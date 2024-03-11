from django.db import models
from profiles.models import User
from datarepo.models import AreaOfInterest


class InnovationChallenge(models.Model):
    industry = models.ForeignKey('profiles.Industry', on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='challenge_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='challenge_updated_by')
    cover_image = models.ImageField(upload_to='challenge_pictures/', blank=True, null=True)
    status = models.CharField(max_length=100,default='active',choices=[
        ('active', 'archived'),
    ])
class InnovationChallengeDetails(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    scenario = models.TextField(blank=True,null=True)

class InnovationTargetBeneficiaries(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

class InnovationChallengeRequirements(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

class InnovationChallengeOperationalCapabilities(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
class InnovationChallengeTangibleOutcomes(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)


class InnovationChallengeOtherRequriments(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    

class InnovationChallengeObjectives(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)


class InnovationChallengeEligibilityCriteria(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
class InnovationChallengeEvaluationCriteria(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    

class InnovationChallengeProposal(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.TextField(blank=True,null=True)
    brief = models.TextField(blank=True,null=True)
    value_proposition = models.TextField(blank=True,null=True)
    solution_readiness = models.TextField(blank=True,null=True)
    implementation_time = models.CharField(max_length=100,blank=True,null=True)
    ip_status =  models.CharField(max_length=100,blank=True,null=True,choices=[('not_applicable', 'not_applicable'),
                                                                                    ('granted', 'granted'),
                                                                                    ('approved', 'approved')
                                                                                    ])
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='proposal_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='proposal_updated_by')

class InnovationChallengeProposalTangibleBenfits(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)


class InnovationChallengeProposalSolutionAdvantages(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

class InnovationChallengeProposalExpertsInvolved(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    role  = models.CharField(max_length=100,blank=True,null=True)

    
class InnovationChallengeProposalFiles(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    document = models.FileField(upload_to='proposal_files/', blank=True, null=True)
    


    