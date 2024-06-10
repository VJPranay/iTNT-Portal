from django.db import models
from django.conf import settings

class MeetingRequest(models.Model):
    MEETING_TYPE_CHOICES = [
        ('online', 'Online'),
        ('offline', 'Offline'),
    ]

    STATUS_CHOICES = [
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    sender = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='sender_sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='reciever_received_requests', on_delete=models.CASCADE)
    date = models.DateField()
    time = models.TimeField()
    meeting_type = models.CharField(max_length=10, choices=MEETING_TYPE_CHOICES)
    meeting_details =  models.CharField(max_length=255, default='')
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='sent')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
