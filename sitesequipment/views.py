from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from sitesequipment.models import SitesEquipment
from sitesequipment.serializers import SitesEquipmentSerializer


class SitesEquipmentListCreateView(generics.ListCreateAPIView):
    queryset = SitesEquipment.objects.all()
    serializer_class = SitesEquipmentSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return SitesEquipment.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SitesEquipmentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SitesEquipment.objects.all()
    serializer_class = SitesEquipmentSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "reference"

    def get_queryset(self):
        return SitesEquipment.objects.filter(user=self.request.user)


class SitesEquipmentListView(generics.ListAPIView):
    queryset = SitesEquipment.objects.all()
    serializer_class = SitesEquipmentSerializer
    permission_classes = [
        AllowAny,
    ]
