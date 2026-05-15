from django.shortcuts import render
from skills.models import Skill, UserSkill
from skills.serializers import SkillSerializer, UserSkillSerializer
from rest_framework import generics, permissions
# Create your views here.

class UserSkills(generics.ListCreateAPIView):
    serializer_class=UserSkillSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    """
    We had to override the create method perform_create() because the generic view
    we are using is List and Create but we want other user to only see different user's
    skills and not add to them.
    So when a POST request will be sent this override will make sure that save occurs
    only when user is the current logged in user.
    perform_create doesn't block creation for other users, 
    it overrides the user field to always be the logged-in user 
    regardless of what was sent in the request body.
    """

    def get_queryset(self):
        queryVal=self.request.query_params.get('user', None)
        if queryVal == None:
            return UserSkill.objects.filter(user=self.request.user)
        return UserSkill.objects.filter(user=queryVal)
    """
    A user should only be able to view their own skills or the skills of a particular User.
    """
    
class SkillDetail(generics.DestroyAPIView):
    serializer_class=UserSkillSerializer

    def get_queryset(self):
        profile=self.request.user
        return UserSkill.objects.filter(user=profile)
    """
    We overrode the get_queryset function because without it an authenticated user would be able to
    any user's skills. The should only be able to delete their own skills.
    """
class SkillList(generics.ListAPIView):
    serializer_class=SkillSerializer
    queryset= Skill.objects.filter(is_approved=True)

class CreateSkill(generics.CreateAPIView):
    serializer_class=SkillSerializer