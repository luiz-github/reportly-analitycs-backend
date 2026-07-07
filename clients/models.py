from django.db import models

from accounts.models import CustomUser
from core.models import SoftDeleteModel

class Client(SoftDeleteModel):
    agency  = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    name    = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)