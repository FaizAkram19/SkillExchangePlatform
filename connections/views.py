from django.shortcuts import render
from connections.models import ConnectionRequest
from connections.serializers import ConnectionRequestSerializer, ConnectionResponseSerializer
from rest_framework import generics, permissions
from django.db.models import Q
from accounts.models import Profile
from accounts.serializers import ProfileSerializer
from skills.models import UserSkill
# Create your views here.

class ListConnections(generics.ListAPIView):
    serializer_class=ConnectionRequestSerializer

    def get_queryset(self):
        """
        We use this view when we want to list the approved connections, now there are two ways connections are accepted
        either the user was a receiver or a sender and the connections status is approved. So we needed to modify the
        filter condition. Now to combine filter conditions in django ORM we need to use Q objects with the |(or),
        &(and), -(not) symbols.
        """
        profile=self.request.user
        return ConnectionRequest.objects.filter((Q(sender=profile) | Q(receiver=profile)) & Q(connectionStatus="a"))
    

class SendRequest(generics.CreateAPIView):
    """
    This view is only used for POSTing connection requests, so it doesn't need a queryset
    to return. It just needs the Create API view. But the create should only go through if
    the sender is the logged in user by default
    """
    serializer_class=ConnectionRequestSerializer
    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

class PendingConnections(generics.ListAPIView):
    serializer_class=ConnectionRequestSerializer
    def get_queryset(self):
        """
        We can easily chain ANDed filter conditions using commas
        """
        profile=self.request.user
        return ConnectionRequest.objects.filter(receiver=profile, connectionStatus="p")
    
class PendingDetail(generics.RetrieveAPIView):
    serializer_class=ConnectionRequestSerializer

    def get_queryset(self):
        profile=self.request.user
        return ConnectionRequest.objects.filter(receiver=profile, connectionStatus="p")

class ResponseView(generics.UpdateAPIView):
    serializer_class=ConnectionResponseSerializer

    def get_queryset(self):
        profile=self.request.user
        return ConnectionRequest.objects.filter(receiver=profile, connectionStatus="p")
    
class SentRequests(generics.ListAPIView):
    serializer_class=ConnectionRequestSerializer
    def get_queryset(self):
        profile=self.request.user
        return ConnectionRequest.objects.filter(sender=profile, connectionStatus="p")
    
class MatchingAlgo(generics.ListAPIView):
    serializer_class=ProfileSerializer
    def get_queryset(self):
        profile=self.request.user
        seeking_ids=UserSkill.objects.filter(user=profile,skill_type="s").values_list('skill', flat=True) 
        eligible1=UserSkill.objects.filter(skill__in=seeking_ids, skill_type="o").values_list('user', flat=True)
        offering_ids=UserSkill.objects.filter(user=profile, skill_type="o").values_list('skill', flat=True)
        eligible2=UserSkill.objects.filter(skill__in=offering_ids, skill_type="s").values_list('user', flat=True)
        find=UserSkill.objects.filter(user__in=eligible1).filter(user__in=eligible2).exclude(user=profile).values_list('user', flat=True)
        return Profile.objects.filter(user__in=find).distinct()




    
