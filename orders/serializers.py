from rest_framework import serializers
from django.db import transaction

from orders.models import Order, OrderItem, OrderStatus, PaymentInstallment
from products.models import Product, PaymentType
from products.serializers import ProductSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    product_details = ProductSerializer(source="product", read_only=True)

    class Meta:
        model = OrderItem
        fields = (
            "id",
            "product",
            "product_details",
            "quantity",
            "price_at_purchase",
            "total_price",
        )
        read_only_fields = ("price_at_purchase", "total_price", "product_name", "sku")


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    buyer_name = serializers.CharField(source="buyer.username", read_only=True)
    supplier_name = serializers.CharField(
        source="supplier_company.name", read_only=True
    )

    # Write choice field for items input
    # Format: [ { "product_reference": "xyz", "quantity": 10 } ]
    cart_items = serializers.JSONField(write_only=True)

    class Meta:
        model = Order
        fields = (
            "id",
            "reference",
            "status",
            "payment_status",
            "selected_payment_type",
            "payment_terms_proposal",
            "total_amount",
            "buyer_name",
            "supplier_name",
            "created_at",
            "items",
            "cart_items",
        )
        read_only_fields = (
            "status",
            "payment_status",
            "total_amount",
            "buyer",
            "buyer_company",
            "supplier_company",
        )

    def validate(self, attrs):
        cart_items = attrs.get("cart_items", [])
        payment_type = attrs.get("selected_payment_type")

        if not cart_items:
            raise serializers.ValidationError("Cart cannot be empty.")

        # Logic: Check if all products allow the selected payment type
        # In a real app, products in one cart should probably belong to one Supplier
        # or we split the order. Here we assume one supplier for simplicity or validate it.

        product_refs = [item["product_reference"] for item in cart_items]
        products = Product.objects.filter(reference__in=product_refs)

        if len(products) != len(product_refs):
            raise serializers.ValidationError("Some products were not found.")

        # Check Payment Compatibility
        for product in products:
            # If payment is NOT Immediate (default), check if product allows it
            if payment_type != PaymentType.IMMEDIATE:
                allowed_options = product.payment_options.values_list(
                    "payment_type", flat=True
                )
                if payment_type not in allowed_options:
                    raise serializers.ValidationError(
                        f"Product '{product.product_name}' does not allow payment method: {payment_type}"
                    )

        # Implicitly setting context for create
        attrs["valid_products"] = {p.reference: p for p in products}

        return attrs

    def create(self, validated_data):
        request = self.context["request"]
        cart_items = validated_data.pop("cart_items")
        products_map = validated_data.pop("valid_products")

        # Determine Supplier (Taking from first product for now)
        first_product_ref = cart_items[0]["product_reference"]
        supplier_company = products_map[first_product_ref].company

        # Calculate Total
        total_amount = 0

        with transaction.atomic():
            order = Order.objects.create(
                buyer=request.user,
                # Assuming user has a company, handle error if not
                buyer_company=getattr(request.user, "company", None),
                supplier_company=supplier_company,
                total_amount=0,  # Update later
                **validated_data,
            )

            items_to_create = []
            for item_data in cart_items:
                product = products_map[item_data["product_reference"]]
                qty = item_data["quantity"]
                price = product.price  # Or logic to fetch price
                line_total = price * qty

                total_amount += line_total

                items_to_create.append(
                    OrderItem(
                        order=order,
                        product=product,
                        product_name=product.product_name,
                        sku=product.sku,
                        quantity=qty,
                        price_at_purchase=price,
                        total_price=line_total,
                    )
                )

            OrderItem.objects.bulk_create(items_to_create)

            order.total_amount = total_amount
            order.save()

            # TODO: If Immediate payment, trigger payment gateway here
            # TODO: If 50/50, generate Installment 1 (Deposit) and Installment 2 (Delivery)

        return order
