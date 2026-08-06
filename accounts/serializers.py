from rest_framework import serializers
from accounts.models import User, Profile
from skills.models import UserSkill
from skills.serializers import UserSkillSerializer


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
    skills_offering=serializers.SerializerMethodField()
    skills_seeking=serializers.SerializerMethodField()

    class Meta:
        model=Profile
        fields=["user","first_name", "last_name", "dp", "timezone", "availability", "rating", "skills_offering", "skills_seeking"]
        extra_kwargs={
            "rating":{'read_only':True}
        }

    

    #In Django REST Framework (DRF), serializers.SerializerMethodField is a read-only field that allows 
    #you to calculate or fetch data dynamically instead of just pulling a raw value straight from a database column.
    #Think of it as a way to create a custom, calculated field on your API response.
    #By default, DRF looks for a method on the serializer class itself to populate the field's data. 
    #That method must follow a strict naming convention: get_<field_name>.


    def get_skills_offering(self, obj):
        qs = UserSkill.objects.filter(user=obj.user, skill_type="o")
        return UserSkillSerializer(qs, many=True).data

    def get_skills_seeking(self, obj):
        qs = UserSkill.objects.filter(user=obj.user, skill_type="s")
        return UserSkillSerializer(qs, many=True).data

    def update(self, instance, validated_data):
        instance.user.first_name = validated_data.get("first_name", instance.user.first_name)
        instance.user.last_name = validated_data.get("last_name", instance.user.last_name)
        instance.user.save()

        instance.timezone=validated_data.get("timezone", instance.timezone)
        instance.availability=validated_data.get("availability", instance.availability)
        instance.save()
        return instance

from django.core.exceptions import ValidationError as DjangoValidationError
from django.contrib.auth.password_validation import validate_password

class PasswordChangeSerializer(serializers.Serializer):
    old_password=serializers.CharField(required=True, write_only=True)
    new_password=serializers.CharField(required=True, write_only=True)

    def validate_old_password(self, value):
        user=self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Password is incorrect")
        return value

    def validate_new_password(self, value):
        try:
            validate_password(value)
        except DjangoValidationError as e:
            raise serializers.ValidationError(list(e.messages))
        return value