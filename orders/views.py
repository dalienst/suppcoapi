from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from orders.models import Order
from orders.serializers import OrderSerializer


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Contractor sees their own orders
        # (Enhancement: For Suppliers, we might need a different view or filtering,
        # but technically Suppliers mostly care about OrderItems.
        # For now, let's assume this view is primarily for the Contractor/User facing side.)
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        user = self.request.user
        # Contractor sees their own orders
        # (Enhancement: For Suppliers, we might need a different view or filtering,
        # but technically Suppliers mostly care about OrderItems.
        # For now, let's assume this view is primarily for the Contractor/User facing side.)
        return Order.objects.filter(user=user)
