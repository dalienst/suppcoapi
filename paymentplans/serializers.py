from rest_framework import serializers
from decimal import Decimal
from paymentplans.models import PaymentPlan
from products.models import Product
from paymentoptions.models import PaymentOption
from paymentplans.utils import (
    calculate_fixed_plan,
    calculate_split_plan,
    calculate_flexible_plan,
)


class PaymentPlanSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="sku"
    )
    payment_option = serializers.SlugRelatedField(
        queryset=PaymentOption.objects.all(), slug_field="reference"
    )

    # Write-only fields for plan calculation
    deposit_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True, required=False
    )
    duration_months = serializers.IntegerField(write_only=True, required=False)

    class Meta:
        model = PaymentPlan
        fields = (
            "reference",
            "product",
            "user",
            "payment_option",
            "amount",
            "plan",
            "created_at",
            "updated_at",
            "deposit_amount",
            "duration_months",
        )
        read_only_fields = ("reference", "amount", "plan", "created_at", "updated_at")

    def validate(self, attrs):
        product = attrs.get("product")
        payment_option = attrs.get("payment_option")
        deposit_amount = attrs.get("deposit_amount", Decimal("0.00"))
        duration_months = attrs.get("duration_months", 0)

        # Basic Validation
        if not product or not payment_option:
            return attrs

        total_amount = product.price
        attrs["amount"] = total_amount  # Set total amount on the model

        # Generate Plan based on Option Type
        if payment_option.is_fixed or payment_option.is_payment_on_delivery:
            attrs["plan"] = calculate_fixed_plan(total_amount)

        elif payment_option.is_split_50_50:
            attrs["plan"] = calculate_split_plan(total_amount)

        elif payment_option.is_flexible:
            # Validate Flexible specific constraints
            if deposit_amount is None:
                raise serializers.ValidationError(
                    {"deposit_amount": "Deposit amount is required for Flexible plans."}
                )

            min_deposit = (payment_option.min_deposit_percentage / 100) * total_amount
            if deposit_amount < min_deposit:
                raise serializers.ValidationError(
                    {
                        "deposit_amount": f"Minimum deposit is {min_deposit} ({payment_option.min_deposit_percentage}%)."
                    }
                )

            if not duration_months or duration_months < 1:
                raise serializers.ValidationError(
                    {"duration_months": "Duration must be at least 1 month."}
                )

            attrs["plan"] = calculate_flexible_plan(
                total_amount, deposit_amount, duration_months
            )

        return attrs

    def create(self, validated_data):
        # Remove write-only fields before creation
        validated_data.pop("deposit_amount", None)
        validated_data.pop("duration_months", None)
        return super().create(validated_data)
