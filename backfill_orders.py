import os
import django

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "suppcoapi.settings")
django.setup()

from orders.models import Order

print("--- Backfilling Order Companies ---")
orders = Order.objects.filter(company__isnull=True)
count = orders.count()
print(f"Found {count} orders without company.")

updated = 0
for order in orders:
    first_item = order.items.first()
    if first_item and first_item.product and first_item.product.company:
        order.company = first_item.product.company
        order.save()
        print(f"Updated Order {order.reference} -> Company: {order.company.name}")
        updated += 1
    else:
        print(f"Skipping Order {order.reference} (No valid item or product company)")

print(f"--- Done. Updated {updated} orders. ---")
