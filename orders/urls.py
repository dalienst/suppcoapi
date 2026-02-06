from django.urls import path
from orders.views import (
    OrderListCreateView,
    OrderRetrieveUpdateDestroyView,
)

app_name = "orders"

urlpatterns = [
    path("", OrderListCreateView.as_view(), name="order-list-create"),
    path(
        "<str:reference>/",
        OrderRetrieveUpdateDestroyView.as_view(),
        name="order-retrieve-update-destroy",
    ),
]
