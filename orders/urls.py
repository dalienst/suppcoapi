from django.urls import path
from orders.views import (
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
    CheckoutView,
)

app_name = "orders"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "<str:reference>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-retrieve-update-destroy",
    ),
]
