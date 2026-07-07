from django.db import models
from django.contrib.auth.models import AbstractUser

from accounts.constants import PLAN_LIMITS
from core.models import SoftDeleteModel

class CustomUser(AbstractUser, SoftDeleteModel):
    agency_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    plan = models.CharField(max_length=50, default="trial")
    plan_starts = models.DateTimeField(null=True, blank=True)
    plan_ends = models.DateTimeField(null=True, blank=True)
    is_active_plan = models.BooleanField(default=False)
    
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
    
    @property
    def has_active_plan(self):
        from django.utils import timezone
        if not self.is_active_plan or not self.plan_ends:
            return False
        return self.plan_ends > timezone.now()
    
    @property
    def client_limit(self):
        return PLAN_LIMITS.get(self.plan, 0)

    @property
    def can_add_client(self):
        from clients.models import Client
        actual = Client.objects.filter(agency=self).count()
        return actual < self.client_limit
    
    
    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email
        super().save(*args, **kwargs)