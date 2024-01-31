from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    user_role = models.IntegerField(choices=[
        (1, 'superadmin'),
        (2, 'admin'),
        (3, 'staff'),
        (4, 'industry'),
        (5, 'researcher'),
        (6, 'startup'),
        (7, 'student'),
        (8, 'vc')]
        ,default=8)
    
