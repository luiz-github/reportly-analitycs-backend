from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from clients.models import Client
from clients.serializers import ClientSerializer

class ClientCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class   = ClientSerializer

    def perform_create(self, serializer):
        if not self.request.user.can_add_client:
            raise PermissionDenied("Plan limit reached. Upgrade to add more clients.")
        serializer.save(agency=self.request.user)
        
class ListClientsView(generics.ListAPIView):
    serializer_class   = ClientSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Client.objects.filter(agency=self.request.user)
    
class DeleteClientView(generics.DestroyAPIView):
    serializer_class = ClientSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return Client.objects.filter(agency_id=self.request.user.id)