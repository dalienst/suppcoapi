from rest_framework import serializers
from orders.models import Order
from orders.serializers import OrderSerializer


class SupplierOrderSerializer(OrderSerializer):
    """
    Serializer for Suppliers to view orders.
    Extends OrderSerializer but can be customized later.
    """

    pass
