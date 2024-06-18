from django.db import models
from profiles.models import User

class HackathonProposal(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    solution_name = models.CharField(max_length=255)
    focus_area = models.CharField(max_length=255)
    team_size = models.IntegerField()
    team_composition = models.TextField()
    solution_brief = models.TextField()
    solution_uniqueness = models.TextField()
    solution_sustainable_development_goals = models.TextField()
    innovation_current_stage = models.CharField(max_length=255)
    patent_status = models.CharField(max_length=255)
    proposed_hackathon_research_papers_exist = models.CharField(max_length=3, choices=[('Yes', 'Yes'), ('No', 'No')])
    proposed_hackathon_research_papers_count = models.IntegerField(null=True, blank=True)
    proposed_hackathon_research_papers_links = models.TextField(null=True, blank=True)
    proposed_hackathon_research_papers_files = models.FileField(upload_to='proposed_hackathon_research_papers/', null=True, blank=True)
    timeframe = models.TextField()
    expected_impacts_outcomes = models.TextField()
    supporting_documents = models.FileField(upload_to='supporting_documents/', null=True, blank=True)
    status = models.CharField(max_length=255,blank=True,null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.solution_name