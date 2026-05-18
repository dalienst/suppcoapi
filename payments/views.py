import json
import hmac
import hashlib
import requests
from decimal import Decimal
from django.conf import settings
from django.http import HttpResponse, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction

from rest_framework import status, permissions
from rest_framework.views import APIView
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentSerializer
from orders.models import Order


class PaymentInitializationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        order_references = request.data.get("order_references", [])

        if not order_references:
            return Response(
                {"error": "Please provide a list of order_references."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 1. Fetch and validate the associated orders
        orders = Order.objects.filter(reference__in=order_references, user=user)
        if not orders.exists():
            return Response(
                {"error": "No matching orders found for this user."},
                status=status.HTTP_404_NOT_FOUND,
            )

        # 2. Calculate dynamic aggregate upfront down payment due across these orders
        total_downpayment = Decimal("0.00")

        for order in orders:
            for item in order.items.all():
                pp = item.payment_plan
                if pp and pp.plan:
                    # Sum the first element in the JSON installment list
                    first_installment = pp.plan[0]
                    total_downpayment += Decimal(str(first_installment.get("amount", 0.00)))
                else:
                    # Fallback to total item amount if no payment plan is set
                    total_downpayment += item.price * item.quantity

        if total_downpayment <= 0:
            return Response(
                {"error": "Initial down payment amount must be greater than zero."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. Create database Payment record in PENDING state
        with transaction.atomic():
            payment = Payment.objects.create(
                user=user,
                amount=total_downpayment,
                status="PENDING",
            )
            payment.orders.set(orders)
            payment.save()

        # 4. Request transaction initialization from Paystack
        paystack_url = "https://api.paystack.co/transaction/initialize"
        headers = {
            "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
            "Content-Type": "application/json",
        }
        
        # Paystack amount is in cents/subunits
        paystack_amount = int(total_downpayment * 100)

        payload = {
            "email": user.email,
            "amount": paystack_amount,
            "reference": payment.reference,
            "callback_url": f"{settings.DOMAIN}/payments/callback/",
            "metadata": {
                "payment_reference": payment.reference,
                "order_references": list(orders.values_list("reference", flat=True)),
            },
            "channels": ["card", "mobile_money"],
        }

        try:
            response = requests.post(paystack_url, json=payload, headers=headers)
            res_data = response.json()

            if response.status_code == 200 and res_data.get("status"):
                return Response(
                    {
                        "payment_reference": payment.reference,
                        "amount": float(total_downpayment),
                        "authorization_url": res_data["data"]["authorization_url"],
                        "access_code": res_data["data"]["access_code"],
                    },
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": res_data.get("message", "Paystack transaction initialization failed.")},
                    status=status.HTTP_424_FAILED_DEPENDENCY,
                )

        except Exception as e:
            return Response(
                {"error": f"Failed to connect to Paystack payment gateway: {str(e)}"},
                status=status.HTTP_502_BAD_GATEWAY,
            )


@method_decorator(csrf_exempt, name="dispatch")
class PaystackWebhookView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # 1. Secure Signature Authentication check
        paystack_signature = request.headers.get("X-Paystack-Signature")
        if not paystack_signature:
            return HttpResponseForbidden("Signature missing")

        # Re-encode body bytes to match exactly
        raw_body = request.body
        calculated_signature = hmac.new(
            settings.PAYSTACK_SECRET_KEY.encode("utf-8"),
            raw_body,
            hashlib.sha512
        ).hexdigest()

        if not hmac.compare_digest(paystack_signature, calculated_signature):
            return HttpResponseForbidden("Signature mismatch")

        # 2. Parse payload event
        try:
            payload = json.loads(raw_body)
        except Exception:
            return Response({"error": "Invalid payload format"}, status=status.HTTP_400_BAD_REQUEST)

        event = payload.get("event")
        if event == "charge.success":
            data = payload.get("data", {})
            ref = data.get("reference")
            
            try:
                with transaction.atomic():
                    # Fetch corresponding payment record
                    payment = Payment.objects.select_for_update().get(reference=ref)
                    
                    if payment.status == "PENDING":
                        # Transition payment state
                        payment.status = "SUCCESS"
                        payment.paystack_reference = data.get("gateway_response") or data.get("reference")
                        payment.payment_method = data.get("channel")
                        payment.metadata = payload
                        payment.save()

                        # Reconcile each linked order and payment plans
                        for order in payment.orders.all():
                            # Calculate downpayment sum specifically for this order
                            order_downpayment = Decimal("0.00")
                            for item in order.items.all():
                                pp = item.payment_plan
                                if pp and pp.plan:
                                    # Update installment 1 state to PAID
                                    pp.plan[0]["status"] = "PAID"
                                    pp.save()
                                    order_downpayment += Decimal(str(pp.plan[0].get("amount", 0.00)))
                                else:
                                    order_downpayment += item.price * item.quantity

                            # Record payment on the order header
                            order.paid_amount += order_downpayment
                            order.status = "PLACED"
                            order.save()

            except Payment.DoesNotExist:
                # Log or handle case where payment is not found (perhaps not initiated by our checkout)
                pass

        return HttpResponse(status=200)
