from django.utils import timezone

from django.db import models
from accounts.models import CustomUser
from clients.models import Client

class PlatformToken(models.Model):
    agency = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    platform = models.CharField(max_length=50)
    access_token = models.CharField(max_length=1000)
    expires_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.agency.agency_name} — {self.platform}"
    
    @property
    def is_connected(self):
        is_connected = self.expires_at > timezone.now()
        return True if is_connected else False
    
class PlatformAccount(models.Model):
    client         = models.ForeignKey(Client, on_delete=models.CASCADE)
    platform_token = models.ForeignKey(PlatformToken, on_delete=models.CASCADE)
    account_id     = models.CharField(max_length=255)
    account_name   = models.CharField(max_length=255, blank=True)
    created_at     = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["client", "platform_token", "account_id"]

    def __str__(self):
        return f"{self.client.name} — {self.account_id}"

    @property
    def platform(self):
        return self.platform_token.platform