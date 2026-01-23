from rest_framework import serializers
from django.db import transaction
from orders.models import Order
from orderitems.models import OrderItem
from orderitems.serializers import OrderItemSerializer
from paymentplans.models import PaymentPlan
from products.models import Product


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = (
            "reference",
            "user",
            "status",
            "total_amount",
            "items",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("total_amount", "reference", "status")

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        user = self.context["request"].user

        # Calculate total amount
        total_amount = 0
        for item in items_data:
            product = item["product"]
            quantity = item["quantity"]
            # Assuming product price is the source of truth
            total_amount += product.price * quantity

        with transaction.atomic():
            order = Order.objects.create(
                user=user, total_amount=total_amount, **validated_data
            )

            for item_data in items_data:
                payment_plan_data = item_data.pop("payment_plan")
                product = item_data["product"]

                # Create PaymentPlan
                # We need to inject user and product into payment_plan_data
                # PaymentPlanSerializer expects 'product' (sku) and 'payment_option' (reference)
                # But here 'payment_plan_data' is validated data from PaymentPlanSerializer
                # which means the slug fields are already converted to model instances.

                payment_plan = PaymentPlan.objects.create(
                    user=user,
                    product=product,  # Product instance from outer item_data
                    payment_option=payment_plan_data["payment_option"],
                    amount=payment_plan_data["amount"],
                    plan=payment_plan_data.get("plan"),
                )

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    payment_plan=payment_plan,
                    quantity=item_data["quantity"],
                    price_at_purchase=product.price,
                )

        return order
