from django.urls import path

from paymentoptions.views import (
    PaymentOptionListCreateAPIView,
    PaymentOptionRetrieveUpdateDestroyAPIView,
)

urlpatterns = [
    path("", PaymentOptionListCreateAPIView.as_view(), name="payment-options"),
    path(
        "<str:reference>/",
        PaymentOptionRetrieveUpdateDestroyAPIView.as_view(),
        name="payment-option",
    ),
]
