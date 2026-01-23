import os
import django
from decimal import Decimal

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suppcoapi.settings")
django.setup()

from django.contrib.auth import get_user_model
from orders.models import Order
from orderitems.models import OrderItem
from products.models import Product
from paymentplans.models import PaymentPlan
from paymentoptions.models import PaymentOption
from companies.models import Company
from branches.models import Branch
from layers.models import Layer
from sublayers.models import SubLayer
from brackets.models import Bracket
from sublayeritems.models import SublayerItem

User = get_user_model()


def verify_orders():
    print("Starting verification...")

    # Clean up possibly previous run
    User.objects.filter(username="test_contractor").delete()

    # 1. Setup Data
    user = User.objects.create_user(
        username="test_contractor", email="test@example.com", password="password123"
    )

    # Create minimal product dependencies
    company = Company.objects.create(name="Test Company", user=user)

    # Create Payment Option
    payment_option = PaymentOption.objects.create(
        user=user, name="Test Option", payment_type="FIXED"
    )

    product = Product.objects.create(
        user=user,
        company=company,
        product_name="Test Product",
        price=Decimal("100.00"),
        quantity=Decimal("10.00"),
    )
    product.payment_options.add(payment_option)

    # Create Payment Plan
    payment_plan = PaymentPlan.objects.create(
        user=user,
        product=product,
        payment_option=payment_option,
        amount=Decimal("100.00"),
    )

    # 2. Create Order
    order = Order.objects.create(user=user, total_amount=Decimal("100.00"))
    print(f"Order created: {order}")

    # 3. Create OrderItem
    order_item = OrderItem.objects.create(
        order=order,
        product=product,
        payment_plan=payment_plan,
        quantity=1,
        price_at_purchase=Decimal("100.00"),
    )
    print(f"OrderItem created: {order_item}")

    # 4. Verify
    assert order.items.count() == 1
    assert order_item.order == order
    assert order_item.product == product

    print("Verification Successful!")


if __name__ == "__main__":
    try:
        verify_orders()
    except Exception as e:
        print(f"Verification Failed: {e}")
