from rest_framework import serializers
from django.db import transaction
from orders.models import Order
from orderitems.models import OrderItem
from orderitems.serializers import OrderItemSerializer
from paymentplans.models import PaymentPlan
from paymentplans.serializers import PaymentPlanSerializer
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
            # ToDo: Handle price logic/discounts here if any
            total_amount += product.price * quantity

        with transaction.atomic():
            order = Order.objects.create(
                user=user, total_amount=total_amount, **validated_data
            )

            for item_data in items_data:
                payment_plan_data = item_data.pop("payment_plan")
                product = item_data["product"]

                # We need to construct the data to pass to PaymentPlanSerializer
                # item_data['product'] is a model instance because of SlugRelatedField in OrderItemSerializer
                # But PaymentPlanSerializer expects data roughly compliant with its fields or we can call save directly if we instantiate validation logic manually?
                # Better approach: Manually call validation logic or re-use serializer?
                # Using serializer is cleaner but we need to re-construct input data or manually call internal methods.
                # Simplest: use the model fields and the utils directly, OR instantiate the serializer with context.

                # Let's instantiate the serializer to leverage the validation logic we just wrote
                pp_serializer = PaymentPlanSerializer(
                    data={
                        "product": product.sku,
                        "payment_option": payment_plan_data["payment_option"].reference,
                        "deposit_amount": payment_plan_data.get("deposit_amount"),
                        "duration_months": payment_plan_data.get("duration_months"),
                        "monthly_amount": payment_plan_data.get("monthly_amount"),
                    },
                    context=self.context,
                )
                pp_serializer.is_valid(raise_exception=True)
                payment_plan = pp_serializer.save(user=user, product=product)

                OrderItem.objects.create(
                    order=order,
                    product=product,
                    payment_plan=payment_plan,
                    quantity=item_data["quantity"],
                    price_at_purchase=product.price,
                )

        return order
