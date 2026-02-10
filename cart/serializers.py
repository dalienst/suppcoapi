from rest_framework import serializers

from cart.models import Cart

from cartitems.serializers import CartItemSerializer


class CartSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.username")
    items = CartItemSerializer(many=True, read_only=True)
    total_amount = serializers.SerializerMethodField()
    total_payable = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = (
            "id",
            "user",
            "total_amount",
            "total_payable",
            "created_at",
            "updated_at",
            "reference",
            "items",
        )

    def get_total_amount(self, obj):
        return sum(item.sub_total for item in obj.items.all())

    def get_total_payable(self, obj):
        return sum(item.payable_amount for item in obj.items.all())
