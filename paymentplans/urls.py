from django.urls import path

from paymentplans.views import (
    PaymentPlanListCreateView,
    PaymentPlanRetrieveUpdateDestroyView,
)

app_name = "paymentplans"

urlpatterns = [
    path("", PaymentPlanListCreateView.as_view()),
    path("<str:reference>/", PaymentPlanRetrieveUpdateDestroyView.as_view()),
]
