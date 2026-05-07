from django.db import models

# Create your models here.
class Skill(models.Model):
    name=models.CharField(max_length=30, unique=True, blank=False)
    description=models.TextField(blank=True)
    is_approved=models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.name=self.name.lower()
        super().save(*args,**kwargs)
    
    def __str__(self):
        return self.name