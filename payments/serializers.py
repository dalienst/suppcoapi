from rest_framework import serializers
from payments.models import Payment
from orders.models import Order


class PaymentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.email", read_only=True)
    order_references = serializers.SerializerMethodField()

    class Meta:
        model = Payment
        fields = (
            "reference",
            "user",
            "amount",
            "paystack_reference",
            "payment_method",
            "status",
            "order_references",
            "created_at",
        )
        read_only_fields = (
            "reference",
            "paystack_reference",
            "payment_method",
            "status",
            "created_at",
        )

    def get_order_references(self, obj):
        return [order.reference for order in obj.orders.all()]
