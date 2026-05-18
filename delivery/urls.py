from django.urls import path
from .views import (
    DeliveryZoneListCreateView,
    DeliveryZoneRetrieveUpdateDestroyView,
)

urlpatterns = [
    # Delivery Zones (Supplier Configuration)
    path("zones/", DeliveryZoneListCreateView.as_view(), name="deliveryzone-list"),
    path("zones/<str:reference>/", DeliveryZoneRetrieveUpdateDestroyView.as_view(), name="deliveryzone-detail"),
]
