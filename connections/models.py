from django.db import models
from accounts.models import User
# Create your models here.
class ConnectionRequest(models.Model):
    status_type={
        "a": "Approved",
        "r": "Rejected",
        "p":"Pending"
    }
    sender=models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_requests")
    receiver=models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_requests")
    connectionStatus=models.CharField(max_length=1, choices=status_type, default="p")

    class Meta:
        unique_together=[["sender", "receiver"]]