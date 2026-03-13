from rest_framework import generics

from inventory.models import Inventory
from inventory.serializers import InventorySerializer
from companies.permissions import IsOwnerOrReadOnly

class InventoryListView(generics.ListAPIView):
    queryset = Inventory.objects.all().prefetch_related("layers")
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    # return only the inventories in that company
    def get_queryset(self):
        if self.request.user.is_supplier or self.request.user.is_contractor:
            return Inventory.objects.filter(company=self.request.user.company)
        return Inventory.objects.all()

class InventoryListCreateView(generics.ListCreateAPIView):
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        if self.request.user.is_supplier or self.request.user.is_contractor:
            return Inventory.objects.filter(company=self.request.user.company)
        return Inventory.objects.all()


class InventoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Inventory.objects.all().prefetch_related("layers")
    serializer_class = InventorySerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "inventory_code"

    # return only the inventories in that company
    def get_queryset(self):
        if self.request.user.is_supplier or self.request.user.is_contractor:
            return Inventory.objects.filter(company=self.request.user.company)
        return Inventory.objects.all()
