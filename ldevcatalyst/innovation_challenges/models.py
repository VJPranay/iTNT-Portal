from django.db import models
from profiles.models import User

# Create your models here.
class ChallengesCategory(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    
class ChallengeSubCategory(models.Model):
    category = models.ForeignKey(ChallengesCategory, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    
class InnovationChallenge(models.Model):
    name = models.CharField(max_length=100,blank=True,null=True)
    challenge_category = models.ForeignKey(ChallengesCategory, on_delete=models.SET_NULL,blank=True,null=True)
    challenges_sub_category = models.ForeignKey(ChallengeSubCategory, on_delete=models.SET_NULL,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='challenge_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='challenge_updated_by')
    cover_image = models.ImageField(upload_to='challenge_pictures/', blank=True, null=True)
    
class InnovationChallengeObjectives(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

class InnovationChallengeEligibilityCriteria(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
class InnovationChallengeEvaluationCriteria(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)

class InnovationChallengeOutcomes(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    

class InnovationChallengeDetails(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    funding_details = models.TextField(blank=True,null=True)
    
    
    
class InnovationChallengeProposal(models.Model):
    challenge = models.ForeignKey(InnovationChallenge, on_delete=models.SET_NULL,blank=True,null=True)
    submitted_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.TextField(blank=True,null=True)
    market_domain = models.CharField(max_length=100,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='proposal_created_by')
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True,null=True,related_name='proposal_updated_by')
    ip_status =  models.CharField(max_length=100,blank=True,null=True,choices=[('not_applicable', 'not_applicable'),
                                                                                    ('granted', 'granted'),
                                                                                    ('approved', 'approved')
                                                                                    ])
class InnovationChallengeProposalBenfits(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
    
class InnovationChallengeProposalMilestones(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    description = models.TextField(blank=True,null=True)
    
class InnovationChallengeProposalTeam(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    mobile = models.CharField(max_length=100,blank=True,null=True)
    email = models.EmailField(blank=True,null=True)
    role = models.CharField(max_length=100,blank=True,null=True)
    
class InnovationChallengeProposalFiles(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=100,blank=True,null=True)
    notes = models.TextField(blank=True,null=True)
    document = models.FileField(upload_to='proposal_files/', blank=True, null=True)
    

class InnovationChallengeProposalDetails(models.Model):
    proposal = models.ForeignKey(InnovationChallengeProposal, on_delete=models.SET_NULL,blank=True,null=True)
    breif = models.TextField(blank=True,null=True)
    value_proposition = models.TextField(blank=True,null=True)
    solution_readiness = models.TextField(blank=True,null=True)
    timeline = models.TextField(blank=True,null=True)
    