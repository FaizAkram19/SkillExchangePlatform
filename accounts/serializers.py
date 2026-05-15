from rest_framework import serializers
from accounts.models import User, Profile

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["id","username", "email", "first_name", "last_name", "password"]
        extra_kwargs={
            "password":{"write_only":True}
        }

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class UserMiniSerializer(serializers.ModelSerializer):
    """
    This serializer only uses the fields that need to be displayed
    """
    class Meta:
        model=User
        fields=["id", "username", "first_name", "last_name"]

class ProfileSerializer(serializers.ModelSerializer):
    # first_name and last_name are declared as explicit write_only fields on ProfileSerializer
    # because they belong to the User model, not Profile. Since user is read_only (to prevent
    # the client from changing which user owns the profile), we can't write to User fields
    # through the nested UserSerializer. Instead we accept them as top-level fields and
    # manually update instance.user in the overridden update() method.
    user=UserSerializer(read_only=True)
    first_name = serializers.CharField(write_only=True, required=False)
    last_name = serializers.CharField(write_only=True, required=False)
    class Meta:
        model=Profile
        fields=["user","first_name", "last_name", "dp", "timezone", "availability", "rating"]
        extra_kwargs={
            "rating":{'read_only':True}
        }
    def update(self, instance, validated_data):
        instance.user.first_name = validated_data.get("first_name", instance.user.first_name)
        instance.user.last_name = validated_data.get("last_name", instance.user.last_name)
        instance.user.save()

        instance.timezone=validated_data.get("timezone", instance.timezone)
        instance.availability=validated_data.get("availability", instance.availability)
        instance.save()
        return instance