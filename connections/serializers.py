from rest_framework import serializers
from connections.models import ConnectionRequest
from accounts.serializers import UserMiniSerializer

class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConnectionRequest
        fields=["sender", "receiver", "connectionStatus"]
        extra_kwargs={
            "sender":{"read_only":True},
            "connectionStatus":{"read_only":True, "default":"p"}
        }
    def validate(self, data):
        sender = self.context['request'].user
        receiver = data['receiver']
        if ConnectionRequest.objects.filter(sender=sender, receiver=receiver).exists():
            raise serializers.ValidationError("Connection request already exists.")
        return data

class ConnectionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConnectionRequest
        fields=["sender", "receiver", "connectionStatus"]
        extra_kwargs={
            "sender":{"read_only":True},
            "receiver":{"read_only":True}
        }

class ConnectionListSerializer(serializers.ModelSerializer):
    sender=UserMiniSerializer(read_only=True)
    receiver=UserMiniSerializer(read_only=True)
    class Meta:
        model=ConnectionRequest
        fields=["id", "sender", "receiver", "connectionStatus"]