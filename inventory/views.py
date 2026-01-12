from rest_framework import generics

from inventory.models import Inventory
from inventory.serializers import InventorySerializer
from companies.permissions import IsOwnerOrReadOnly

class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.all().prefetch_related("layers")
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]

class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Inventory.objects.filter(user=self.request.user)


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all().prefetch_related("layers")
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "inventory_code"
