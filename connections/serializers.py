from rest_framework import serializers
from connections.models import ConnectionRequest

class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConnectionRequest
        fields=["sender", "receiver", "connectionStatus"]
        extra_kwargs={
            "sender":{"read_only":True},
            "connectionStatus":{"read_only":True, "default":"p"}
        }

class ConnectionResponseSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConnectionRequest
        fields=["sender", "receiver", "connectionStatus"]
        extra_kwargs={
            "sender":{"read_only":True},
            "receiver":{"read_only":True}
        }