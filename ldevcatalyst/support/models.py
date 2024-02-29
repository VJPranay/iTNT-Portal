from django.db import models

class SupportRequest(models.Model):
    name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    mobile = models.CharField(max_length=100)
    account_role = models.CharField(max_length=100)
    support_category = models.CharField(max_length=100)
    short_description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)