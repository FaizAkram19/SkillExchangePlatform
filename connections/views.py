from django.shortcuts import render
from connections.models import ConnectionRequest
from connections.serializers import ConnectionRequestSerializer
from rest_framework import generics, permissions
from django.db.models import Q
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
        profile=self.request.user
        """
        We can easily chain ANDed filter conditions using commas
        """
        return ConnectionRequest.objects.filter(receiver=profile, connectionStatus="p")
    





    
