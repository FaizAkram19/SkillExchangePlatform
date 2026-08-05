from django.contrib import admin
from .models import ConnectionRequest


@admin.register(ConnectionRequest)
class ConnectionRequestAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "connectionStatus")
    list_filter = ("connectionStatus",)
    search_fields = ("sender__username", "receiver__username")