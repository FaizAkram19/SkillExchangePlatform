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
    RetrieveUpdateAPIView expects a pk in the URL to look up a single object. But since you're always fetching the 
    logged-in user's own profile, you don't need a pk at all — you need to override get_object instead.
    """
    def get_object(self):
        return self.request.user.profile