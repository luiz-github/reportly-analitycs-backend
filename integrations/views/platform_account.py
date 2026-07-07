from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from integrations.serializers.PlatformAccountSerializer import PlatformAccountSerializer

class PlatformAccountCreateView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = PlatformAccountSerializer