from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from integrations.models import PlatformToken
from integrations.serializers.PlatformTokenSerializer import PlatformTokenSerializer

class ConnectedIntegrationsView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class=PlatformTokenSerializer
    
    def get_queryset(self):
        return PlatformToken.objects.filter(agency_id=self.request.user.id)
    
class DisconnectIntegrationView(generics.DestroyAPIView):
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return PlatformToken.objects.filter(agency_id=self.request.user.id)