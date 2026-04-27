from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class User(AbstractUser):
    pass 

class Profile(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE)
    dp=models.URLField(blank=True)
    timezone=models.CharField(max_length=25, default='Asia/Kolkata')
    availability=models.JSONField(default=dict)
    rating=models.DecimalField(max_digits=3, decimal_places=2, default=None, null=True)