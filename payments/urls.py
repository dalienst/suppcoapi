from django.urls import path
from payments.views import PaymentInitializationView, PaystackWebhookView, PaymentListView

app_name = "payments"

urlpatterns = [
    path("", PaymentListView.as_view(), name="list"),
    path("initialize/", PaymentInitializationView.as_view(), name="initialize"),
    path("webhook/", PaystackWebhookView.as_view(), name="webhook"),
]
