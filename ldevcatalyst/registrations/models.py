from django.db import models
from datarepo.models import AreaOfInterest,PreferredInvestmentStage,Department,Institution,District,State,IndustryCategory



class Patent(models.Model):
    number = models.CharField(max_length=50,blank=True, null=True)
    title = models.CharField(max_length=255,blank=True, null=True)
    inventors = models.CharField(max_length=255,blank=True, null=True)
    filing_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return self.title

class Publication(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    paper_link = models.URLField(blank=True, null=True)
    journal = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.title

class VC(models.Model):
    partner_name = models.CharField(max_length=100,blank=True, null=True)
    firm_name = models.CharField(max_length=100,blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    contact_number = models.CharField(max_length=15,blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL,blank=True, null=True)
    area_of_interest = models.ForeignKey(AreaOfInterest, on_delete=models.SET_NULL,blank=True, null=True)
    preferred_investment_stage = models.ForeignKey(PreferredInvestmentStage, on_delete=models.SET_NULL,blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.partner_name

class Researcher(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL,blank=True, null=True)
    email_id = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15,blank=True, null=True)
    picture = models.ImageField(upload_to='researcher_pictures/', blank=True, null=True)
    research_areas = models.ManyToManyField(AreaOfInterest)
    highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    patents = models.ForeignKey(Patent, on_delete=models.SET_NULL, blank=True, null=True)
    publications = models.ForeignKey(Publication, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.name
    
class StartUp(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    co_founder_count = models.PositiveIntegerField(blank=True, null=True)
    founder_names = models.CharField(max_length=255,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    team_size = models.PositiveIntegerField(blank=True, null=True)
    email_address = models.EmailField(blank=True, null=True)
    mobile_number = models.CharField(max_length=15,blank=True, null=True)
    website = models.URLField(blank=True, null=True)

    dpiit_number = models.CharField(max_length=20,blank=True, null=True)
    area_of_interest = models.ForeignKey(AreaOfInterest, on_delete=models.SET_NULL,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    funding_stage = models.ForeignKey(PreferredInvestmentStage, on_delete=models.SET_NULL,blank=True, null=True)
    pitch_deck = models.FileField(upload_to='pitch_decks/', blank=True, null=True)
    video_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name
    
    
class Student(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    domain_of_interest = models.ManyToManyField(AreaOfInterest)

    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    year_of_graduation = models.PositiveIntegerField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)

    project_idea = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name



class Industry(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    industry = models.ForeignKey(IndustryCategory, on_delete=models.SET_NULL,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    district = models.ForeignKey(District,on_delete=models.SET_NULL,blank=True,null=True)
    
    point_of_contact_name = models.CharField(max_length=100,blank=True, null=True)
    poc_mail_id = models.EmailField(blank=True, null=True)
    poc_contact_number = models.CharField(max_length=15,blank=True, null=True)

    area_of_interest_for_collaboration = models.ManyToManyField(AreaOfInterest)

    def __str__(self):
        return self.name