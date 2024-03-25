from django.db import models
from profiles.models import VC, StartUp
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.utils import timezone

class MeetingRequests(models.Model):
    start_up = models.ForeignKey(StartUp, on_delete=models.SET_NULL, blank=True, null=True)
    vc = models.ForeignKey(VC, on_delete=models.SET_NULL, blank=True, null=True)
    message = models.TextField(blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('start_up_request', 'start_up_request'),
        ('vc_accepted','vc_accepted'),
        ('scheduled', 'scheduled'),
        ('online_meeting_link_awaiting', 'online_meeting_link_awaiting'),
        ('start_up_reschedule','start_up_reschedule'),
        ('rejected', 'rejected'),
    ])
    meeting_type = models.CharField(max_length=50, blank=True, null=True, choices=[
        ('online', 'online'),
        ('offline', 'offline'),
    ])
    meeting_location = models.TextField(blank=True, null=True)
    meeting_date = models.DateField(blank=True, null=True)
    meeting_time = models.TimeField(blank=True, null=True)
    meeting_date_time = models.DateTimeField(blank=True, null=True)
    next_level = models.CharField(max_length=255, blank=True, null=True)

@receiver(pre_save, sender=MeetingRequests)
def update_meeting_date_time(sender, instance, **kwargs):
    # Check if both meeting_date and meeting_time have values
    if instance.meeting_date and instance.meeting_time:
        # Combine meeting_date and meeting_time to create meeting_date_time
        combined_datetime = timezone.datetime.combine(instance.meeting_date, instance.meeting_time)
        instance.meeting_date_time = combined_datetime
