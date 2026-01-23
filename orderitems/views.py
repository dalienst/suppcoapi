from rest_framework import generics, permissions
from orderitems.models import OrderItem
from orderitems.serializers import OrderItemSerializer


class OrderItemListCreateView(generics.ListCreateAPIView):
    # Mostly read-only for now, possibly update status later
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Users see items from their orders
        # TODO: Add logic for Suppliers to see items they need to fulfill
        return OrderItem.objects.filter(order__user=user)


class OrderItemRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderItemSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        user = self.request.user
        # Users see items from their orders
        # TODO: Add logic for Suppliers to see items they need to fulfill
        return OrderItem.objects.filter(order__user=user)
