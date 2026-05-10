from django.shortcuts import render
from accounts.models import Profile, User
from rest_framework import generics
from accounts.serializers import ProfileSerializer, UserSerializer
from rest_framework import permissions
# Create your views here.

class createUser(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=UserSerializer
    permission_classes=[permissions.AllowAny]
    """
    We had to use the allow any permissions on createUser because the global default in settings is
    permissions.IsAuthenticated which would not let any user create an account cause they aren't already
    authenticated.
    """

class userProfile(generics.RetrieveUpdateAPIView):
    serializer_class=ProfileSerializer
    permission_classes=[permissions.IsAuthenticated]
    """
    Since we only need the authenticated user's Profile and nothing else, we can't simply use
    quesryset, since we need dynamic filtering as a different User will be making the request
    each time. We need to override the get_quesryset method.
    """
    def get_queryset(self):
        profile=self.request.user
        return Profile.objects.filter(user=profile) # filter instead of get because get_queryset expects a queryset(duh)