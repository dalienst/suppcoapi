from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.db import transaction
from django.shortcuts import get_object_or_404

from orders.models import Order
from orders.serializers import OrderSerializer
from orderitems.models import OrderItem
from cart.models import Cart
from paymentplans.serializers import PaymentPlanSerializer
from paymentoptions.models import PaymentOption


class OrderListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Contractor sees their own orders
        # (Enhancement: For Suppliers, we might need a different view or filtering,
        # but technically Suppliers mostly care about OrderItems.
        # For now, let's assume this view is primarily for the Contractor/User facing side.)
        return Order.objects.filter(user=user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class OrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        user = self.request.user
        # Contractor sees their own orders
        # (Enhancement: For Suppliers, we might need a different view or filtering,
        # but technically Suppliers mostly care about OrderItems.
        # For now, let's assume this view is primarily for the Contractor/User facing side.)
        return Order.objects.filter(user=user)


class CheckoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        user = request.user
        cart = get_object_or_404(Cart, user=user)
        # Select related fields for grouping and data access
        cart_items = cart.items.select_related(
            "product", "product__company", "payment_option"
        ).all()

        if not cart_items.exists():
            return Response(
                {"error": "Cart is empty"}, status=status.HTTP_400_BAD_REQUEST
            )

        # 1. Validate Stock Globally
        for item in cart_items:
            # Assuming product has a 'quantity' field for stock
            if item.quantity > item.product.quantity:
                return Response(
                    {"error": f"Not enough stock for {item.product.product_name}"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        created_orders = []

        with transaction.atomic():
            # 2. Group Items by (Company, PaymentOption)
            # using a dictionary to group
            grouped_items = {}
            for item in cart_items:
                # Use references for grouping keys to be safe and consistent
                key = (item.product.company.reference, item.payment_option.reference)
                if key not in grouped_items:
                    grouped_items[key] = []
                grouped_items[key].append(item)

            # 3. Create Order for each group
            for key, items in grouped_items.items():
                # All items in this group share the same supplier and payment option
                # We can grab it from the first item
                first_item = items[0]
                # In strict theory, payment options might differ slightly but here we grouped by strict reference
                # so they are the same option.

                # Create Order
                order = Order.objects.create(
                    user=user,
                    status="PLACED",
                    total_amount=0,
                )

                total_order_amount = 0

                for item in items:
                    product = item.product

                    # Generate Payment Plan
                    pp_data = {
                        "product": product.sku,
                        "payment_option": item.payment_option.reference,
                        "deposit_amount": item.deposit_amount,
                        "duration_months": item.duration_months,
                    }

                    pp_context = {"request": request}
                    pp_serializer = PaymentPlanSerializer(
                        data=pp_data, context=pp_context
                    )

                    if not pp_serializer.is_valid():
                        # Should not happen if cart validation is good, but safety check
                        raise ValueError(
                            f"Invalid payment plan for {product.product_name}: {pp_serializer.errors}"
                        )

                    payment_plan = pp_serializer.save(user=user, product=product)

                    # Create OrderItem
                    OrderItem.objects.create(
                        order=order,
                        product=product,
                        payment_plan=payment_plan,
                        quantity=item.quantity,
                        price_at_purchase=product.price,
                    )

                    total_order_amount += product.price * item.quantity

                    # Deduct Stock
                    product.quantity -= item.quantity
                    product.save()

                # Update Order Total
                order.total_amount = total_order_amount
                order.save()
                created_orders.append(order)

            # 4. Clear Cart
            cart.items.all().delete()

        # Return list of created orders
        return Response(
            OrderSerializer(created_orders, many=True).data,
            status=status.HTTP_201_CREATED,
        )
