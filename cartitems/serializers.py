from rest_framework import serializers

from cartitems.models import CartItem
from products.models import Product
from cart.models import Cart


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.SlugRelatedField(
        slug_field="reference", queryset=Product.objects.all()
    )
    cart = serializers.CharField(read_only=True, source="cart.reference")
    sub_total = serializers.ReadOnlyField()

    class Meta:
        model = CartItem
        fields = (
            "cart",
            "product",
            "quantity",
            "sub_total",
            "created_at",
            "updated_at",
            "reference",
        )

    def validate(self, attrs):
        product = attrs.get("product")
        quantity = attrs.get("quantity")

        if product.stock < quantity:
            raise serializers.ValidationError("Stock is not enough")

        if quantity <= 0:
            pass

        if not product and self.instance:
            product = self.instance.product

        return attrs

    def create(self, validated_data):
        cart = Cart.objects.get(user=self.context["request"].user)
        validated_data["cart"] = cart

        # check if the product is already in the cart
        if CartItem.objects.filter(
            cart=cart, product=validated_data["product"]
        ).exists():
            # update the quantity
            cart_item = CartItem.objects.get(
                cart=cart, product=validated_data["product"]
            )
            cart_item.quantity += validated_data["quantity"]
            cart_item.save()
        else:
            # create a new cart item
            cart_item = CartItem.objects.create(**validated_data)
        return cart_item

    def update(self, instance, validated_data):
        instance.quantity = validated_data.get("quantity", instance.quantity)
        if instance.quantity == 0:
            instance.delete()
            return instance
        instance.save()
        return instance
