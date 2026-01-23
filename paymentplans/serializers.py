from rest_framework import serializers

from paymentplans.models import PaymentPlan
from products.models import Product
from paymentoptions.models import PaymentOption


class PaymentPlanSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="sku"
    )
    payment_option = serializers.SlugRelatedField(
        queryset=PaymentOption.objects.all(), slug_field="reference"
    )

    class Meta:
        model = PaymentPlan
        fields = (
            "product",
            "user",
            "payment_option",
            "amount",
            "plan",
            "created_at",
            "updated_at",
            "reference",
        )
