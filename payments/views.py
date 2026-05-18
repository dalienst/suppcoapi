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

from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response

from payments.models import Payment
from payments.serializers import PaymentSerializer
from orders.models import Order


class PaymentListView(generics.ListAPIView):
    serializer_class = PaymentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Payment.objects.filter(user=self.request.user).order_by("-created_at")


class PaymentInitializationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        plan_reference = request.data.get("plan_reference", None)
        installment_index = request.data.get("installment_index", None)

        if plan_reference is not None and installment_index is not None:
            from paymentplans.models import PaymentPlan
            try:
                payment_plan = PaymentPlan.objects.get(reference=plan_reference, user=user)
            except PaymentPlan.DoesNotExist:
                return Response(
                    {"error": "Payment plan not found."},
                    status=status.HTTP_404_NOT_FOUND,
                )

            try:
                inst_idx = int(installment_index)
                installment = payment_plan.plan[inst_idx]
            except (IndexError, ValueError, TypeError):
                return Response(
                    {"error": "Invalid installment index."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            if installment.get("status") == "PAID":
                return Response(
                    {"error": "This installment has already been paid."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            amount = Decimal(str(installment.get("amount", 0.00)))
            if amount <= 0:
                return Response(
                    {"error": "Installment amount must be greater than zero."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Find matching order
            order_item = getattr(payment_plan, "order_item", None)
            order = order_item.order if order_item else None
            orders = [order] if order else []

            # Create Database Payment
            with transaction.atomic():
                payment = Payment.objects.create(
                    user=user,
                    amount=amount,
                    status="PENDING",
                )
                if orders:
                    payment.orders.set(orders)

                # Set custom metadata
                payment.metadata = {
                    "payment_type": "INSTALLMENT",
                    "plan_reference": plan_reference,
                    "installment_index": inst_idx,
                }
                payment.save()

            # Request Paystack initialization
            paystack_url = "https://api.paystack.co/transaction/initialize"
            headers = {
                "Authorization": f"Bearer {settings.PAYSTACK_SECRET_KEY}",
                "Content-Type": "application/json",
            }
            paystack_amount = int(amount * 100)

            payload = {
                "email": user.email,
                "amount": paystack_amount,
                "reference": payment.reference,
                "callback_url": f"{settings.DOMAIN}/payments/callback/",
                "metadata": {
                    "payment_reference": payment.reference,
                    "payment_type": "INSTALLMENT",
                    "plan_reference": plan_reference,
                    "installment_index": inst_idx,
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
                            "amount": float(amount),
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
            # Add shipping fee for this order if present
            try:
                if hasattr(order, "delivery_detail") and order.delivery_detail:
                    total_downpayment += order.delivery_detail.shipping_fee
            except Exception:
                pass

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
                        payment.paystack_reference = data.get("reference")
                        payment.payment_method = data.get("channel")
                        
                        paystack_metadata = data.get("metadata", {})
                        payment.metadata = paystack_metadata
                        payment.save()

                        # Reconcile Payment
                        if paystack_metadata.get("payment_type") == "INSTALLMENT":
                            from paymentplans.models import PaymentPlan
                            plan_ref = paystack_metadata.get("plan_reference")
                            inst_idx = int(paystack_metadata.get("installment_index"))
                            
                            payment_plan = PaymentPlan.objects.get(reference=plan_ref)
                            payment_plan.plan[inst_idx]["status"] = "PAID"
                            payment_plan.save()
                            
                            # Increment Order's paid_amount
                            order_item = getattr(payment_plan, "order_item", None)
                            if order_item:
                                order = order_item.order
                                order.paid_amount += payment.amount
                                order.save()
                        else:
                            # Standard checkout bulk payments
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

                                # Include shipping fee in total paid amount
                                shipping_fee = Decimal("0.00")
                                try:
                                    if hasattr(order, "delivery_detail") and order.delivery_detail:
                                        shipping_fee = order.delivery_detail.shipping_fee
                                except Exception:
                                    pass

                                # Record payment on the order header
                                order.paid_amount += (order_downpayment + shipping_fee)
                                order.status = "PLACED"
                                order.save()

            except Payment.DoesNotExist:
                # Log or handle case where payment is not found (perhaps not initiated by our checkout)
                pass

        return HttpResponse(status=200)
