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
    
    #validate() is DRF's object-level validation hook — it runs after all individual field validations pass, 
    #and it gets the full dict of validated field data so you can check things that involve multiple fields together
    #After sender, receiver, connectionStatus have each individually passed their own validation (type checks, required checks, etc.),
    #DRF calls validate(self, data) with data = the cleaned dict of all fields.
    def validate(self, data):

        #Since sender is read_only, it's not even in data — it never comes from the client. 
        #So you pull it from the request context instead (this is the standard pattern for "set this field to the logged-in user").
        sender = self.context['request'].user

        #Grabs the receiver that the client submitted.
        receiver = data['receiver']

        #Queries the DB to see if a ConnectionRequest with this exact sender+receiver pair already exists.
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