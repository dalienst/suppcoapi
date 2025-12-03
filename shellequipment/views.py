from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from shellequipment.models import ShellEquipment
from shellequipment.serializers import ShellEquipmentSerializer


class ShellEquipmentListCreateView(generics.ListCreateAPIView):
    queryset = ShellEquipment.objects.all()
    serializer_class = ShellEquipmentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return ShellEquipment.objects.filter(user=self.request.user)


class ShellEquipmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ShellEquipment.objects.all()
    serializer_class = ShellEquipmentSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "reference"

    def get_queryset(self):
        return ShellEquipment.objects.filter(user=self.request.user)


class ShellEquipmentListView(generics.ListAPIView):
    queryset = ShellEquipment.objects.all()
    serializer_class = ShellEquipmentSerializer
    permission_classes = [
        AllowAny,
    ]
