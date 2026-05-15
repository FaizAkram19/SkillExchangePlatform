from rest_framework import serializers
from skills.models import Skill, UserSkill

class SkillSerializer(serializers.ModelSerializer):
    is_approved=serializers.BooleanField(read_only=True)
    # is_approved is read_only so that the user doesn't bypass it
    class Meta:
        model=Skill
        fields=["name", "description", "is_approved"]
    
class UserSkillSerializer(serializers.ModelSerializer):
    skill=serializers.PrimaryKeyRelatedField(queryset=Skill.objects.all())
    class Meta:
        model=UserSkill
        fields=["id", "skill", "skill_type"]
        # no user in the fields cause it'll be automatically saved in the view
    def to_representation(self, instance):
        rep=super().to_representation(instance)
        rep['skill']=SkillSerializer(instance.skill).data
        return rep
    