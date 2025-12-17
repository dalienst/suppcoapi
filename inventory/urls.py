from django.urls import path

from inventory.views import InventoryListCreateView, InventoryDetailView

app_name = "inventory"

urlpatterns = [
    path("", InventoryListCreateView.as_view(), name="inventory-list-create"),
    path(
        "<str:inventory_code>/",
        InventoryDetailView.as_view(),
        name="inventory-detail",
    ),
]
