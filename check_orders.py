import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suppcoapi.settings")
django.setup()

from orders.models import Order
from companies.models import Company
from django.contrib.auth import get_user_model

User = get_user_model()

print("--- Checking Orders ---")
orders = Order.objects.all()
print(f"Total Orders: {orders.count()}")

for order in orders:
    print(f"Order {order.reference}: User={order.user.email}, Company={order.company}")
    if not order.company and order.items.exists():
        first_item = order.items.first()
        print(
            f"  -> Has items. First item product company: {first_item.product.company}"
        )

print("\n--- Checking Users/Companies ---")
for user in User.objects.all():
    try:
        updated_company = user.company
        print(f"User {user.email} owns {updated_company.name}")
    except Exception:
        pass

    employer_companies = user.employees.all()
    if employer_companies.exists():
        print(f"User {user.email} works for: {[c.name for c in employer_companies]}")
