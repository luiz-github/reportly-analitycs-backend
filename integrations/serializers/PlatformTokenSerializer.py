from rest_framework import serializers
from integrations.models import PlatformToken

class PlatformTokenSerializer(serializers.ModelSerializer):
    is_connected = serializers.ReadOnlyField()

    class Meta:
        model = PlatformToken
        exclude = ["access_token"]