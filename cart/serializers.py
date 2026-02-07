from rest_framework import serializers

from cart.models import Cart


class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.username")
    items = OrderItemSerializer(many=True, read_only=True)
    total_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, read_only=True
    )

    class Meta:
        model = Cart
        fields = ["__all__"]
