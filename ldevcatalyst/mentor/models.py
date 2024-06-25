from django.db import models
from datarepo.models import AreaOfInterest,State,District
import uuid
# Create your models here.


class MentorRegistration(models.Model):
    name=models.CharField(max_length=255,blank=True,null=True)
    mobile=models.CharField(max_length=255,blank=True,null=True)
    address=models.CharField(max_length=255,blank=True,null=True)
    email=models.EmailField(max_length=255,blank=True,null=True)
    gender = models.CharField(max_length=100,choices=[('male','Male'),('female','Female'), ('prefer not to say','Prefer not to say')],blank=True, null=True)
    profile_picture=models.ImageField(upload_to='mentor_profile_pictures/',blank=True,null=True)
    company_name=models.CharField(max_length=255,blank=True,null=True)
    designation=models.CharField(max_length=255,blank=True,null=True)
    linkedin_url=models.CharField(max_length=255,blank=True,null=True)
    updated_bio=models.FileField(upload_to='mentor_bios/',blank=True,null=True)
    certified_mentor=models.BooleanField(null=True,blank=True)
    reason=models.CharField(max_length=255,blank=True,null=True)
    area_of_interest=models.ForeignKey(AreaOfInterest, on_delete=models.SET_NULL, null=True, blank=True)
    functional_areas_of_expertise=models.CharField(max_length=255,blank=True,null=True)
    mentoring_experience=models.CharField(max_length=255,blank=True,null=True) 
    motivation_for_mentoring=models.CharField(max_length=255,blank=True,null=True)
    category_represent_you=models.CharField(max_length=255,blank=True,null=True)
    mentees_journey=models.CharField(max_length=255,blank=True,null=True)
    #new
    commitment_as_mentor=models.CharField(max_length=255,blank=True,null=True)
    intensive_mentoring_program=models.CharField(max_length=255,blank=True,null=True) # Intensive mentoring program
    state = models.ForeignKey(State, on_delete=models.SET_NULL, blank=True, null=True)
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True, null=True)
    #end new
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    registration_id = models.CharField(max_length=100,unique=True,null=True)
    status = models.CharField(
        max_length=10,
        choices=[('pending', 'pending'), ('approved', 'approved'), ('rejected', 'rejected')],
        default='pending',
    )
    
    def save(self, *args, **kwargs):
        if not self.registration_id:
            # Generate a unique registration ID
            self.registration_id = 'MNRG-' + str(uuid.uuid4())[:4].upper()  # Using part of UUID to ensure uniqueness
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural="MentorRegistration" 
    