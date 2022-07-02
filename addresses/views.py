import django.db.utils
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response


from addresses.models import Address
from addresses.serializers import AddressSerializer


class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def handle_exception(self, exc):
        if isinstance(exc, django.db.utils.IntegrityError):
            return Response({'error': 'Duplicated address'}, status=status.HTTP_400_BAD_REQUEST)
        return super().handle_exception(exc)
