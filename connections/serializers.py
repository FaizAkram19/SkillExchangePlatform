from rest_framework import serializers
from connections.models import ConnectionRequest

class ConnectionRequestSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConnectionRequest
        fields=["sender", "receiver", "connectionStatus"]
        extra_kwargs={
            "sender":{"read_only":True}
        }