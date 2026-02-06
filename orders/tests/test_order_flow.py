from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from decimal import Decimal
from datetime import date
from orders.models import Order
from products.models import Product
from companies.models import Company
from paymentoptions.models import PaymentOption
from paymentplans.models import PaymentPlan

User = get_user_model()


class OrderPaymentFlowTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password")
        self.client.force_authenticate(user=self.user)

        # Setup Company and Product
        self.company = Company.objects.create(name="Test Company", user=self.user)
        self.product = Product.objects.create(
            user=self.user,
            company=self.company,
            product_name="Test Product",
            price=Decimal("10000.00"),
            sku="TP-001",
        )

        # Setup Payment Options
        self.option_fixed = PaymentOption.objects.create(
            user=self.user, name="Fixed", payment_type="FIXED"
        )

        self.option_flexible = PaymentOption.objects.create(
            user=self.user,
            name="Flexible",
            payment_type="FLEXIBLE",
            min_deposit_percentage=Decimal("20.00"),
        )

    def test_create_order_with_fixed_payment(self):
        data = {
            "items": [
                {
                    "product": self.product.sku,
                    "quantity": 1,
                    "payment_plan": {"payment_option": self.option_fixed.reference},
                }
            ]
        }

        response = self.client.post("/api/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(reference=response.data["reference"])
        self.assertEqual(order.items.count(), 1)

        item = order.items.first()
        plan = item.payment_plan

        # Verify plan logic
        self.assertEqual(len(plan.plan), 1)
        self.assertEqual(plan.plan[0]["amount"], 10000.0)

    def test_create_order_with_flexible_payment(self):
        data = {
            "items": [
                {
                    "product": self.product.sku,
                    "quantity": 1,
                    "payment_plan": {
                        "payment_option": self.option_flexible.reference,
                        "deposit_amount": "3000.00",  # 30%
                        "duration_months": 2,
                    },
                }
            ]
        }

        response = self.client.post("/api/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(reference=response.data["reference"])
        item = order.items.first()
        plan = item.payment_plan

        # Verify plan: 1 deposit + 2 installments = 3 entries
        self.assertEqual(len(plan.plan), 3)
        self.assertEqual(plan.plan[0]["description"], "Deposit")
        self.assertEqual(plan.plan[0]["amount"], 3000.0)

        # Remaining: 7000 / 2 = 3500
        self.assertEqual(plan.plan[1]["amount"], 3500.0)
        self.assertEqual(plan.plan[2]["amount"], 3500.0)

    def test_flexible_payment_validation(self):
        # Try with too low deposit
        data = {
            "items": [
                {
                    "product": self.product.sku,
                    "quantity": 1,
                    "payment_plan": {
                        "payment_option": self.option_flexible.reference,
                        "deposit_amount": "1000.00",  # 10% (min is 20%)
                        "duration_months": 2,
                    },
                }
            ]
        }

        response = self.client.post("/api/orders/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        # Verify error message usually buried in response data
        # Check that we handled the validation error from serializer

    def test_add_item_to_cart(self):
        # 1. Get Cart (should create new DRAFT)
        response = self.client.get("/api/orders/cart/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["status"], "DRAFT")
        order_ref = response.data["reference"]

        # 2. Add Item to Cart
        data = {
            "product": self.product.sku,
            "quantity": 2,
            "payment_plan": {"payment_option": self.option_fixed.reference},
        }
        response = self.client.post("/api/orders/cart/items/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # 3. Verify Order Total updated
        response = self.client.get("/api/orders/cart/")
        self.assertEqual(response.data["total_amount"], "20000.00")  # 10000 * 2
