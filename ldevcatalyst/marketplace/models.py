from django.db import models
from profiles.models import StartUp
# Create your models here.


class Products(models.Model):
    start_up = models.ForeignKey(StartUp, on_delete=models.SET_NULL,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    breif = models.TextField(blank=True, null=True)
    value_proposition = models.TextField(blank=True, null=True)
    solution_advantage = models.TextField(blank=True, null=True)
    product_readiness = models.TextField(blank=True, null=True)
    implementation_time = models.TextField(blank=True, null=True)
    ip_status = models.CharField(max_length=100,blank=True, null=True,choices=[
        ('not_applicable', 'not_applicable'), 
        ('granted', 'granted'), 
        ('published', 'published'), 
        ('expired', 'expired'), ] )
    
    class Meta:
        verbose_name_plural ="Products"                        
    
class ProductBenfits(models.Model):
    product = models.ForeignKey(Products, on_delete=models.SET_NULL,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    class Meta:
        verbose_name_plural ="ProductBenfits"
class Services(models.Model):
    start_up = models.ForeignKey(StartUp, on_delete=models.SET_NULL,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100,blank=True, null=True)
    breif = models.TextField(blank=True, null=True)
    value_proposition = models.TextField(blank=True, null=True)
    solution_advantage = models.TextField(blank=True, null=True)
    service_readiness = models.TextField(blank=True, null=True)
    implementation_time = models.TextField(blank=True, null=True)
    ip_status = models.CharField(max_length=100,blank=True, null=True,choices=[
        ('not_applicable', 'not_applicable'), 
        ('granted', 'granted'), 
        ('published', 'published'), 
        ('expired', 'expired'), ] )
    class Meta:
        verbose_name_plural ="Services"
    
class TangibleBenfits(models.Model):
    product = models.ForeignKey(Services, on_delete=models.SET_NULL,blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    
    class Meta:
        verbose_name_plural ="TangibleBenfits"