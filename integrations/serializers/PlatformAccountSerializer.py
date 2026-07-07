from rest_framework import serializers
from integrations.models import PlatformAccount

class PlatformAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlatformAccount
        fields = "__all__"