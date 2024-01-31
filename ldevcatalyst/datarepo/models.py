from django.db import models

# Create your models here.
class AreaOfInterest(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class PreferredInvestmentStage(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Institution(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class State(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class IndustryCategory(models.Model):
    name = models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.name
