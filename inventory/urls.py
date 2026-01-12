from django.urls import path

from inventory.views import (
    InventoryListCreateView,
    InventoryDetailView,
    InventoryListView,
)

app_name = "inventory"

urlpatterns = [
    path("", InventoryListView.as_view(), name="inventory-list"),
    path(
        "list-create/", InventoryListCreateView.as_view(), name="inventory-list-create"
    ),
    path(
        "<str:inventory_code>/",
        InventoryDetailView.as_view(),
        name="inventory-detail",
    ),
]
