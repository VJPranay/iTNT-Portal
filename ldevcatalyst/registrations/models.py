from django.db import models
from datarepo.models import AreaOfInterest,PreferredInvestmentStage,Department,Institution,District,State,IndustryCategory
import uuid


class PatentInfo(models.Model):
    number = models.CharField(max_length=50,blank=True, null=True)
    title = models.CharField(max_length=255,blank=True, null=True)
    inventors = models.CharField(max_length=255,blank=True, null=True)
    filing_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50,blank=True, null=True)

    def __str__(self):
        return self.title

class PublicationInfo(models.Model):
    title = models.CharField(max_length=255,blank=True, null=True)
    paper_link = models.URLField(blank=True, null=True)
    journal = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.title

class VCRegistrations(models.Model):
    partner_name = models.CharField(max_length=100,blank=True, null=True)
    firm_name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15,blank=True, null=True)
    deal_size_range = models.CharField(max_length=255,blank=True, null=True)
    portfolio_size = models.PositiveIntegerField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL,blank=True, null=True)
    area_of_interest = models.ForeignKey(AreaOfInterest, on_delete=models.SET_NULL,blank=True, null=True)
    funding_stage = models.ForeignKey(PreferredInvestmentStage, on_delete=models.SET_NULL,blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    registration_id = models.CharField(max_length=100,unique=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')],
        default='pending',
    )
    def save(self, *args, **kwargs):
        if not self.registration_id:
            # Generate a unique registration ID
            self.registration_id = 'VCRG-' + str(uuid.uuid4())[:4].upper()  # Using part of UUID to ensure uniqueness
        super().save(*args, **kwargs)

    # def __str__(self):
    #     return self.partner_name

class ResearcherRegistrations(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15,blank=True, null=True)
    picture = models.ImageField(upload_to='researcher_pictures/', blank=True, null=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest)
    highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    patents = models.ForeignKey(PatentInfo, on_delete=models.SET_NULL, blank=True, null=True)
    publications = models.ForeignKey(PublicationInfo, on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    registration_id = models.CharField(max_length=100,unique=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')],
        default='pending',
    )
    def save(self, *args, **kwargs):
        if not self.registration_id:
            # Generate a unique registration ID
            self.registration_id = 'RCRG-' + str(uuid.uuid4())[:4].upper()  # Using part of UUID to ensure uniqueness
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class StartUpRegistrations(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    co_founder_count = models.PositiveIntegerField(blank=True, null=True)
    founder_names = models.CharField(max_length=255,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    team_size = models.PositiveIntegerField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15,blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    dpiit_number = models.CharField(max_length=20,blank=True, null=True)
    area_of_interest = models.ForeignKey(AreaOfInterest, on_delete=models.SET_NULL,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    market_size = models.CharField(max_length=20,blank=True, null=True)
    required_amount = models.CharField(max_length=255,blank=True, null=True)
    founding_year = models.PositiveIntegerField(blank=True, null=True)
    founding_experience = models.BooleanField(blank=True, null=True)
    funding_stage = models.ForeignKey(PreferredInvestmentStage, on_delete=models.SET_NULL,blank=True, null=True)
    pitch_deck = models.CharField(max_length=100,blank=True, null=True)
    video_link = models.CharField(max_length=100,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    registration_id = models.CharField(max_length=100,unique=True)
    short_video =  models.URLField(blank=True, null=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')],
        default='pending',
    )
    def save(self, *args, **kwargs):
        if not self.registration_id:
            # Generate a unique registration ID
            self.registration_id = 'SURG-' + str(uuid.uuid4())[:4].upper()  # Using part of UUID to ensure uniqueness
        super().save(*args, **kwargs)


    # def __str__(self):
    #     return self.name
    
    
class StudentRegistrations(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    year_of_graduation = models.PositiveIntegerField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    project_idea = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    registration_id=models.CharField(max_length=100,unique=True,null=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')],
        default='pending',
    )
    def save(self, *args, **kwargs):
        if not self.registration_id:
            # Generate a unique registration ID
            self.registration_id = 'SDRG-' + str(uuid.uuid4())[:4].upper()  # Using part of UUID to ensure uniqueness
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}-{self.status}-{self.institution}-{self.year_of_graduation},{self.district}-{self.state}-{self.department}'



class IndustryRegistrations(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)
    industry = models.ForeignKey(IndustryCategory, on_delete=models.SET_NULL,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    district = models.ForeignKey(District,on_delete=models.SET_NULL,blank=True,null=True)
    point_of_contact_name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=15,blank=True, null=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    registration_id = models.CharField(max_length=100,unique=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')],
        default='pending',
    )
    def save(self, *args, **kwargs):
        if not self.registration_id:
            # Generate a unique registration ID
            self.registration_id = 'INRG-' + str(uuid.uuid4())[:4].upper()  # Using part of UUID to ensure uniqueness
        super().save(*args, **kwargs)