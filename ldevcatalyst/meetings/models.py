from django.db import models
from profiles.models import VC,StartUp

# Create your models here.
class MeetingRequests(models.Model):
    start_up = models.ForeignKey(StartUp, on_delete=models.SET_NULL,blank=True, null=True)
    vc = models.ForeignKey(VC, on_delete=models.SET_NULL,blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50,blank=True, null=True,choices=[
        ('pending', 'pending'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    ])
    
