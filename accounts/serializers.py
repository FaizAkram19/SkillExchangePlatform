from rest_framework import serializers
from accounts.models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username", "email", "first_name", "last_name", "password"]

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProfileSerializer(serializers.ModelSerializer):
    user=UserSerializer()
    class Meta:
        model=Profile
        fields=["user", "dp", "timezone", "availability", "rating"]
        extra_kwargs={
            "rating":{'read_only':True}
        }