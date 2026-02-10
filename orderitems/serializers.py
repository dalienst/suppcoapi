from rest_framework import serializers
from orderitems.models import OrderItem
from products.models import Product
from paymentplans.serializers import PaymentPlanSerializer
from paymentplans.models import PaymentPlan


class OrderItemPaymentPlanSerializer(PaymentPlanSerializer):
    """
    Simplified serializer for creating a PaymentPlan within an Order.
    Product and User are injected by the backend.
    """

    payment_option_name = serializers.CharField(
        source="payment_option.name", read_only=True
    )

    class Meta(PaymentPlanSerializer.Meta):
        fields = (
            "payment_option",
            "payment_option_name",
            "amount",
            "plan",
            "deposit_amount",
            "duration_months",
            "total_interest",
        )
        read_only_fields = ("amount", "plan", "payment_option_name", "total_interest")


class OrderItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="reference"
    )
    product_reference = serializers.CharField(
        read_only=True, source="product.reference"
    )
    product_name = serializers.CharField(read_only=True, source="product.product_name")
    product_sku = serializers.CharField(read_only=True, source="product.sku")
    product_company = serializers.CharField(
        read_only=True, source="product.company.name"
    )
    payment_plan = OrderItemPaymentPlanSerializer()

    class Meta:
        model = OrderItem
        fields = (
            "reference",
            "product",
            "product_name",
            "product_reference",
            "product_sku",
            "product_company",
            "payment_plan",
            "quantity",
            "price_at_purchase",
            "status",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("price_at_purchase", "reference", "status")

    def create(self, validated_data):
        # This create method might not be called directly if using nested writes from Order
        # but good to have logic here or rely on OrderSerializer to handle it.
        # Ideally, we handle logic in OrderSerializer for the full creation flow.
        pass
