from django.db import models

# Create your models here.
class AreaOfInterest(models.Model):
    name = models.CharField(max_length=255)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_approved_categories():
        return AreaOfInterest.objects.filter(is_approved=True)

class PreferredInvestmentStage(models.Model):
    name = models.CharField(max_length=255)
    serial = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    

class RevenueStage(models.Model):
    name = models.CharField(max_length=255)
    serial = models.IntegerField(default=0)

    def __str__(self):
        return self.name
    
class ProductDevelopmentStage(models.Model):
    name = models.CharField(max_length=255)
    serial = models.IntegerField(default=0)
    description = models.CharField(max_length=255)

    def __str__(self):
        return self.name
    

class PrimaryBusinessModel(models.Model):
    name = models.CharField(max_length=255)
    serial = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class District(models.Model):
    state = models.ForeignKey(State, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class IndustryCategory(models.Model):
    name = models.CharField(max_length=255,blank=True, null=True)

    def __str__(self):
        return self.name

class Institution(models.Model):
    district = models.ForeignKey(District, on_delete=models.SET_NULL,blank=True,null=True)
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name