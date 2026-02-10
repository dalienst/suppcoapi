from django.urls import path
from .views import SupplierOrderListCreateView, SupplierOrderRetrieveUpdateDestroyView

urlpatterns = [
    path("", SupplierOrderListCreateView.as_view(), name="supplier-orders-list"),
    path(
        "<str:reference>/",
        SupplierOrderRetrieveUpdateDestroyView.as_view(),
        name="supplier-orders-detail",
    ),
]
