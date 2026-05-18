from django.urls import path
from .views import (
    OrderDeliveryListCreateView,
    OrderDeliveryRetrieveUpdateDestroyView,
    VerifyDeliveryPinView,
)

urlpatterns = [
    # Order Deliveries (Tracking & Statuses)
    path("", OrderDeliveryListCreateView.as_view(), name="orderdelivery-list"),
    path("<str:reference>/", OrderDeliveryRetrieveUpdateDestroyView.as_view(), name="orderdelivery-detail"),
    path("<str:reference>/verify-pin/", VerifyDeliveryPinView.as_view(), name="orderdelivery-verify-pin"),
]
