from rest_framework import serializers

from cartitems.models import CartItem
from products.models import Product
from cart.models import Cart
from paymentoptions.models import PaymentOption


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="reference", queryset=Product.objects.all()
    )
    cart = serializers.CharField(read_only=True, source="cart.reference")
    sub_total = serializers.ReadOnlyField()
    payment_option = serializers.SlugRelatedField(
        slug_field="reference", queryset=PaymentOption.objects.all()
    )

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

        # 1. Product Stock Validation
        if product and quantity:
            if product.stock < quantity:
                raise serializers.ValidationError({"quantity": "Stock is not enough"})

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
                if deposit_amount is None:
                    raise serializers.ValidationError(
                        {
                            "deposit_amount": "Deposit amount is required for Flexible plans."
                        }
                    )

                # Check min deposit percentage
                min_deposit = (
                    payment_option.min_deposit_percentage / 100
                ) * product.price
                if deposit_amount < min_deposit:
                    raise serializers.ValidationError(
                        {
                            "deposit_amount": f"Minimum deposit is {min_deposit} ({payment_option.min_deposit_percentage}% of price)."
                        }
                    )

                if not duration_months or duration_months < 1:
                    raise serializers.ValidationError(
                        {"duration_months": "Duration must be at least 1 month."}
                    )

        if not product and self.instance:
            product = self.instance.product

        return attrs

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

        if instance.quantity <= 0:
            instance.delete()
            return instance

        instance.save()
        return instance
