from django.urls import path

from orderitems.views import OrderItemListCreateView, OrderItemRetrieveUpdateDestroyView

app_name = "orderitems"

urlpatterns = [
    path("", OrderItemListCreateView.as_view(), name="orderitem-list-create"),
    path(
        "<str:reference>/",
        OrderItemRetrieveUpdateDestroyView.as_view(),
        name="orderitem-retrieve-update-destroy",
    ),
]
