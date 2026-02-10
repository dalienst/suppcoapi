from rest_framework import serializers
from decimal import Decimal
from paymentplans.models import PaymentPlan
from products.models import Product
from paymentoptions.models import PaymentOption
from paymentplans.utils import (
    calculate_fixed_plan,
    calculate_split_plan,
    calculate_flexible_plan,
    calculate_flexible_plan_by_amount,
)


class PaymentPlanSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    total_interest = serializers.SerializerMethodField()
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(), slug_field="sku"
    )

    def get_total_interest(self, obj):
        if not obj.plan:
            return 0

        total_payable = sum(Decimal(str(item["amount"])) for item in obj.plan)
        principal = (
            obj.product.price
        )  # PaymentPlan is usually for 1 item unit? OR full order?
        # Check model: PaymentPlan usually tracks a specific product purchase.
        # But PaymentPlan model doesn't seem to store quantity?
        # Let's check PaymentPlan model.
        # Warning: If PaymentPlan is linked to OrderItem, quantity matters.
        # But PaymentPlan itself has 'amount' (total valid amount).
        # Let's use obj.amount which was set to total_amount in validate logic.

        # In validate: total_amount = product.price.
        # So Principal is obj.amount?
        # But obj.amount in serializer usually refers to the field.
        # Let's assume Principal = obj.amount (if that stores the cash price)
        # OR calculate from Plan - Principal.

        # Actually, let's look at how amount is set.
        # In validate: attrs["amount"] = total_amount = product.price
        # So obj.amount IS the principal (Cash Price).

        principal = obj.amount
        interest = total_payable - principal
        return max(interest, 0)

    payment_option = serializers.SlugRelatedField(
        queryset=PaymentOption.objects.all(), slug_field="reference"
    )

    # Write-only fields for plan calculation
    deposit_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True, required=False
    )
    duration_months = serializers.IntegerField(
        write_only=True, required=False, allow_null=True
    )
    monthly_amount = serializers.DecimalField(
        max_digits=10, decimal_places=2, write_only=True, required=False
    )

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
            "monthly_amount",
            "total_interest",
        )
        read_only_fields = ("reference", "amount", "plan", "created_at", "updated_at")

    def validate(self, attrs):
        product = attrs.get("product")
        payment_option = attrs.get("payment_option")
        deposit_amount = attrs.get("deposit_amount", Decimal("0.00"))
        duration_months = attrs.get("duration_months", 0)
        monthly_amount = attrs.get("monthly_amount", Decimal("0.00"))

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

            if monthly_amount and monthly_amount > 0:
                interest_rate = payment_option.interest_rate or 0
                attrs["plan"] = calculate_flexible_plan_by_amount(
                    total_amount, deposit_amount, monthly_amount, interest_rate
                )
            elif duration_months and duration_months >= 1:
                interest_rate = payment_option.interest_rate or 0
                attrs["plan"] = calculate_flexible_plan(
                    total_amount, deposit_amount, duration_months, interest_rate
                )
            else:
                raise serializers.ValidationError(
                    "For Flexible plans, you must provide either a duration (in months) or a monthly installment amount."
                )

        return attrs

    def create(self, validated_data):
        # Remove write-only fields before creation
        validated_data.pop("deposit_amount", None)
        validated_data.pop("duration_months", None)
        validated_data.pop("monthly_amount", None)
        return super().create(validated_data)
