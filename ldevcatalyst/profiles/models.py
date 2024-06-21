from django.db import models
from django.contrib.auth.models import AbstractUser
from datarepo.models import AreaOfInterest,PreferredInvestmentStage,Department,Institution,District,State,IndustryCategory, FundRaised, PrimaryBusinessModel, ProductDevelopmentStage, RevenueStage
from mentor.models import MentorRegistration
from django.core.exceptions import ValidationError


class User(AbstractUser):
    user_role = models.IntegerField(choices=[
        (1, 'superadmin'),
        (2, 'admin'),
        (3, 'staff'),
        (4, 'industry'),
        (5, 'researcher'),
        (6, 'startup'),
        (7, 'student'),
        (8, 'vc'),
        (9, 'mentor')
        ]
        ,default=8)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    


class Patent(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    number = models.CharField(max_length=50,blank=True, null=True)
    title = models.CharField(max_length=255,blank=True, null=True)
    inventors = models.CharField(max_length=255,blank=True, null=True)
    filing_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=50,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

class Publication(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    title = models.CharField(max_length=255,blank=True, null=True)
    paper_link = models.URLField(blank=True, null=True)
    journal = models.CharField(max_length=100,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    


def validate_file_size(value):
    """
    Validate that the file size is less than or equal to 20MB (20 * 1024 * 1024 bytes).
    """
    max_size = 20 * 1024 * 1024  # 20MB in bytes
    if value.size > max_size:
        raise ValidationError('File size cannot exceed 20MB.')

class VC(models.Model):
    FUND_TYPE_CHOICES = [
        ('angel_investor', 'Angel Investor'),
        ('angel_network', 'Angel Network'),
        ('venture_capital', 'Venture Capital Fund'),
        ('family_office', 'Family Office'),
        ('corporate_vc', 'Corporate Venture Capital'),
    ]
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    partner_name = models.CharField(max_length=255,blank=True, null=True)
    firm_name = models.CharField(max_length=255,blank=True, null=True)
    designation = models.CharField(max_length=100,blank=True, null=True)
    name = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=255,blank=True, null=True)
    deal_size_range_min = models.PositiveIntegerField(blank=True, null=True)
    deal_size_range_max = models.PositiveIntegerField(blank=True, null=True)
    deal_size_range=models.PositiveBigIntegerField(blank=True, null=True)
    deal_size_range_usd = models.PositiveBigIntegerField(blank=True, null=True)
    portfolio_size = models.PositiveIntegerField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL,blank=True, null=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest, blank=True, null=True)
    funding_stage = models.ManyToManyField(PreferredInvestmentStage, blank=True, null=True)
    company_website = models.URLField(blank=True, null=True)
    linkedin_profile = models.URLField(blank=True, null=True)
    fund_type = models.CharField(max_length=255, null=True, blank=True, default=None, choices=FUND_TYPE_CHOICES)
    company_portfolio_document = models.FileField(upload_to='portfolio_documents/', validators=[validate_file_size], blank=True, null=True)

    data_source = models.CharField(max_length=255, null=True, blank=True)
    approved = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.partner_name

class Researcher(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL,blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL,blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL,blank=True, null=True)
    gender = models.IntegerField(choices=[(1,'Male'),(2,'Female'), (3, 'Prefer not to say')],blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=255,blank=True, null=True)
    picture = models.ImageField(upload_to='researcher_pictures/', blank=True, null=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest)
    highest_qualification = models.CharField(max_length=100, blank=True, null=True)
    patents = models.ManyToManyField(Patent, blank=True, null=True)
    publications = models.ForeignKey(Publication, on_delete=models.SET_NULL, blank=True, null=True)
    
    data_source = models.CharField(max_length=225,blank=True, null=True)
    approved = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
    
class StartUp(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    company_name = models.CharField(max_length=255,blank=True, null=True)
    co_founders_count = models.PositiveIntegerField(blank=True, null=True)
    founder_names = models.CharField(max_length=255,blank=True, null=True)
    team_size = models.PositiveIntegerField(blank=True, null=True)
    funding_request_amount = models.CharField(max_length=100,blank=True, null=True)
    year_of_establishment = models.PositiveIntegerField(blank=True, null=True)
    dpiit_number = models.CharField(max_length=20,blank=True, null=True)
    company_description = models.TextField(blank=True, null=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    area_of_interest = models.ForeignKey(AreaOfInterest, on_delete=models.SET_NULL,blank=True, null=True)
    preferred_investment_stage = models.ForeignKey(PreferredInvestmentStage, on_delete=models.SET_NULL,blank=True, null=True)
    fund_raised = models.ForeignKey(FundRaised, on_delete=models.SET_NULL,blank=True, null=True)
    fund_raised_input = models.CharField(max_length=255,blank=True, null=True)
    primary_business_model = models.ForeignKey(PrimaryBusinessModel, on_delete=models.SET_NULL,blank=True, null=True)
    incubators_associated = models.CharField(max_length=255,blank=True, null=True)
    client_customer_size = models.CharField(max_length=255,blank=True, null=True)
    reveune_stage = models.ForeignKey(RevenueStage, on_delete=models.SET_NULL,blank=True, null=True)
    development_stage = models.ForeignKey(ProductDevelopmentStage, on_delete=models.SET_NULL,blank=True, null=True)
    development_stage_document = models.FileField(upload_to='development_stage_document/', blank=True, null=True)
    company_website = models.CharField(max_length=255,blank=True, null=True)
    company_linkedin = models.CharField(max_length=500,blank=True, null=True)
    video_link = models.CharField(max_length=255,blank=True, null=True)
    pitch_deck = models.FileField(upload_to='pitch_decks/', blank=True, null=True)
    company_logo = models.FileField(upload_to='company_logo/', blank=True, null=True)
    #poc details
    linkedin = models.CharField(max_length=255,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=255,blank=True, null=True)
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'), ('prefer not to say', 'Prefer not to say')],blank=True, null=True) 
    # details
    data_source = models.CharField(max_length=255,blank=True, null=True)
    approved = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.company_name
    
    
class Student(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    institution = models.ForeignKey(Institution, on_delete=models.SET_NULL, null=True, blank=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest)
    email=models.EmailField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    year_of_graduation = models.PositiveIntegerField(blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL, null=True, blank=True)
    state = models.ForeignKey(State, on_delete=models.SET_NULL, null=True, blank=True)
    project_idea = models.TextField(blank=True, null=True)
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'), ('prefer not to say', 'Prefer not to say')],blank=True, null=True)
    mobile = models.CharField(max_length=255,blank=True, null=True)
    project_guide_name = models.CharField(max_length=255,blank=True, null=True)
    highest_qualification = models.CharField(max_length=255,blank=True, null=True)
    paper_published = models.CharField(max_length=255,blank=True, null=True)


    data_source = models.CharField(max_length=255,blank=True, null=True)
    approved = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name



class Industry(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    industry = models.ForeignKey(IndustryCategory, on_delete=models.SET_NULL,blank=True,null=True)
    state = models.ForeignKey(State,on_delete=models.SET_NULL,blank=True,null=True)
    district = models.ForeignKey(District,on_delete=models.SET_NULL,blank=True,null=True)
    point_of_contact_name = models.CharField(max_length=100,blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    mobile = models.CharField(max_length=255,blank=True, null=True)
    area_of_interest = models.ManyToManyField(AreaOfInterest)
    
    data_source = models.CharField(max_length=255,blank=True, null=True)
    approved = models.BooleanField(default=False)

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    
class Mentor(models.Model):
    user=models.ForeignKey(User, on_delete=models.SET_NULL,blank=True, null=True)
    name=models.CharField(max_length=255,blank=True,null=True)
    mobile=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(max_length=255,blank=True,null=True)
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'), ('prefer not to say','Prefer not to say')],blank=True, null=True)
    profile_picture=models.ImageField(upload_to='mentor_profile_pictures',blank=True,null=True)
    company_name=models.CharField(max_length=255,blank=True,null=True)
    designation=models.CharField(max_length=255,blank=True,null=True)
    linkedin_url=models.CharField(max_length=255,blank=True,null=True)
    updated_bio=models.FileField(upload_to='mentor_bios',blank=True,null=True)
    certified_mentor=models.BooleanField(null=True,blank=True)
    area_of_interest=models.ForeignKey(AreaOfInterest, on_delete=models.SET_NULL, null=True, blank=True)
    functional_areas_of_expertise=models.CharField(max_length=255,blank=True,null=True)
    mentoring_experience=models.CharField(max_length=255,blank=True,null=True) 
    motivation_for_mentoring=models.CharField(max_length=255,blank=True,null=True)
    category_represent_you=models.CharField(max_length=255,blank=True,null=True)
    mentees_journey=models.CharField(max_length=255,blank=True,null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    approved=models.BooleanField(default=False)
    
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="Mentor" 
    
    
