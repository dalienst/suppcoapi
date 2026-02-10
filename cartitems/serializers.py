from rest_framework import serializers

from cartitems.models import CartItem
from products.models import Product
from cart.models import Cart
from paymentoptions.models import PaymentOption
from paymentplans.utils import (
    calculate_flexible_plan,
    calculate_flexible_plan_by_amount,
)


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="reference", queryset=Product.objects.all()
    )
    cart = serializers.CharField(read_only=True, source="cart.reference")
    sub_total = serializers.ReadOnlyField()
    payment_option = serializers.SlugRelatedField(
        slug_field="reference", queryset=PaymentOption.objects.all()
    )
    projections = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = (
            "cart",
            "product",
            "quantity",
            "sub_total",
            "payment_option",
            "deposit_amount",
            "duration_months",
            "monthly_amount",
            "projections",
            "created_at",
            "updated_at",
            "reference",
        )

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")
        payment_option = attrs.get("payment_option")
        deposit_amount = attrs.get("deposit_amount")
        duration_months = attrs.get("duration_months")
        monthly_amount = attrs.get("monthly_amount")

        if self.instance:
            if not product:
                product = self.instance.product
            if not quantity:
                quantity = self.instance.quantity
            if not payment_option:
                payment_option = self.instance.payment_option
            if deposit_amount is None:
                deposit_amount = self.instance.deposit_amount
            # duration_months usually optional/nullable so we check if key exists or use instance?
            # attrs.get returns None if missing. If we want to validate logic involving duration, we might need it.
            if "duration_months" not in attrs:
                duration_months = self.instance.duration_months
            if "monthly_amount" not in attrs:
                monthly_amount = self.instance.monthly_amount
        else:
            # If creating new item and quantity is missing, default to 1 as per model
            if not quantity:
                quantity = 1
                attrs["quantity"] = 1

        # 1. Product quantity Validation
        if product and quantity:
            if product.quantity < quantity:
                raise serializers.ValidationError(
                    {"quantity": "quantity is not enough"}
                )

        # 2. Payment Option Validation
        if payment_option and product:
            # Check if this payment option is allowed for this product
            if not product.payment_options.filter(id=payment_option.id).exists():
                raise serializers.ValidationError(
                    {
                        "payment_option": f"Payment option '{payment_option.name}' is not available for this product."
                    }
                )

            # 3. Flexible Payment Validation
            if payment_option.is_flexible:
                total_price = product.price * quantity
                min_deposit = (
                    payment_option.min_deposit_percentage / 100
                ) * total_price
                formatted_min_deposit = "{:,.2f}".format(min_deposit)
                formatted_total_price = "{:,.2f}".format(total_price)

                if deposit_amount is None:
                    raise serializers.ValidationError(
                        {
                            "deposit_amount": (
                                f"Deposit amount is required for Flexible plans. "
                                f"The minimum required is {formatted_min_deposit} "
                                f"({payment_option.min_deposit_percentage}% of {formatted_total_price})."
                            )
                        }
                    )

                if deposit_amount < min_deposit:
                    formatted_min_deposit = "{:,.2f}".format(min_deposit)
                    formatted_total_price = "{:,.2f}".format(total_price)
                    raise serializers.ValidationError(
                        {
                            "deposit_amount": (
                                f"The minimum required deposit is {formatted_min_deposit} "
                                f"({payment_option.min_deposit_percentage}% of the total price {formatted_total_price}). "
                                f"You provided {deposit_amount}."
                            )
                        }
                    )

                has_duration = duration_months and duration_months >= 1
                has_monthly_amount = monthly_amount and monthly_amount > 0

                if not has_duration and not has_monthly_amount:
                    raise serializers.ValidationError(
                        "For Flexible plans, you must provide either a duration (in months) or a monthly installment amount."
                    )

                remaining_after_deposit = (product.price * quantity) - deposit_amount
                if has_monthly_amount and monthly_amount > remaining_after_deposit:
                    raise serializers.ValidationError(
                        {
                            "monthly_amount": "Monthly amount cannot be greater than the remaining balance."
                        }
                    )

        return attrs

    def get_projections(self, obj):
        if not obj.payment_option or not obj.payment_option.is_flexible:
            return None

        # Calculate total based on current quantity
        total_amount = obj.product.price * obj.quantity
        deposit = obj.deposit_amount or 0

        if obj.monthly_amount and obj.monthly_amount > 0:
            return calculate_flexible_plan_by_amount(
                total_amount, deposit, obj.monthly_amount
            )
        elif obj.duration_months and obj.duration_months > 0:
            return calculate_flexible_plan(total_amount, deposit, obj.duration_months)

        return None

    def create(self, validated_data):
        cart = Cart.objects.get(user=self.context["request"].user)
        validated_data["cart"] = cart

        # check if the product with same payment option is already in the cart
        # (Different payment options might imply separate cart items in some logic,
        # but user likely wants to update existing item if just changing quantity?
        # Let's assume distinct line items if payment terms differ?
        # For simplicity, if product exists in cart, we update it, overwriting old payment terms
        # UNLESS we want to support multiple configs for same product.
        # Given "suppco" context, let's treat (product) as unique key in cart for now.)

        cart_item = CartItem.objects.filter(
            cart=cart, product=validated_data["product"]
        ).first()

        if cart_item:
            # update quantity and payment terms
            cart_item.quantity += validated_data["quantity"]
            cart_item.payment_option = validated_data.get(
                "payment_option", cart_item.payment_option
            )
            cart_item.deposit_amount = validated_data.get(
                "deposit_amount", cart_item.deposit_amount
            )
            cart_item.duration_months = validated_data.get(
                "duration_months", cart_item.duration_months
            )
            cart_item.monthly_amount = validated_data.get(
                "monthly_amount", cart_item.monthly_amount
            )
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(**validated_data)

        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        instance.payment_option = validated_data.get(
            "payment_option", instance.payment_option
        )
        instance.deposit_amount = validated_data.get(
            "deposit_amount", instance.deposit_amount
        )
        instance.duration_months = validated_data.get(
            "duration_months", instance.duration_months
        )
        instance.monthly_amount = validated_data.get(
            "monthly_amount", instance.monthly_amount
        )

        if instance.quantity <= 0:
            instance.delete()
            return instance

        instance.save()
        return instance
