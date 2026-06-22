from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.db.models import Q

from .models import OrderDelivery
from .serializers import OrderDeliverySerializer
from orders.models import Order


class OrderDeliveryListCreateView(generics.ListCreateAPIView):
    serializer_class = OrderDeliverySerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Contractor sees deliveries for their orders
        # Supplier sees deliveries for orders placed with their company
        try:
            owned_company = user.company
        except Exception:
            owned_company = None

        employer_companies = user.employees.all()

        return OrderDelivery.objects.filter(
            Q(order__user=user) | 
            Q(order__company=owned_company) | 
            Q(order__company__in=employer_companies)
        ).distinct()


class OrderDeliveryRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = OrderDeliverySerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        user = self.request.user
        try:
            owned_company = user.company
        except Exception:
            owned_company = None

        employer_companies = user.employees.all()

        return OrderDelivery.objects.filter(
            Q(order__user=user) | 
            Q(order__company=owned_company) | 
            Q(order__company__in=employer_companies)
        ).distinct()


class VerifyDeliveryPinView(APIView):
    """
    Suppliers/drivers can verify the Contractor's 6-digit delivery PIN
    to mark the shipment/pickup as COMPLETED.
    """
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, reference):
        user = request.user
        delivery = get_object_or_404(OrderDelivery, reference=reference)

        # Ensure the user belongs to the supplier company that owns this order
        try:
            owned_company = user.company
        except Exception:
            owned_company = None
        employer_companies = list(user.employees.all())

        allowed_companies = []
        if owned_company:
            allowed_companies.append(owned_company)
        allowed_companies.extend(employer_companies)

        if delivery.order.company not in allowed_companies:
            return Response(
                {"error": "Unauthorized. Only the supplying company can verify delivery of this order."},
                status=status.HTTP_403_FORBIDDEN
            )

        pin = request.data.get("pin")
        if not pin:
            return Response(
                {"error": "Please provide the 6-digit verification PIN from the contractor."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if delivery.secure_pin != pin:
            return Response(
                {"error": "Invalid verification PIN code. Delivery cannot be completed."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Update both the Delivery and the underlying Order statuses atomically
        delivery.status = "COMPLETED"
        delivery.save()

        order = delivery.order
        order.status = "COMPLETED"
        order.save()

        return Response(
            {
                "success": "PIN verified successfully. Order and Delivery marked as COMPLETED.",
                "delivery_status": delivery.status,
                "order_status": order.status
            },
            status=status.HTTP_200_OK
        )
