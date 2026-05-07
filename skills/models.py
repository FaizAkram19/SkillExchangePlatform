from django.db import models
from accounts.models import User

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
    

class UserSkill(models.Model):
    SKILL_CHOICE={
        "s": "Seeking",
        "o": "Offering",
    }
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    skill=models.ForeignKey(Skill, on_delete=models.CASCADE)
    skill_type=models.CharField(max_length=1, choices=SKILL_CHOICE)

    def __str__(self):
        return self.skill.name
    
    class Meta:
        unique_together=[["user", "skill", "skill_type"]]