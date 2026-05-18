from django.urls import path
from payments.views import PaymentInitializationView, PaystackWebhookView

app_name = "payments"

urlpatterns = [
    path("initialize/", PaymentInitializationView.as_view(), name="initialize"),
    path("webhook/", PaystackWebhookView.as_view(), name="webhook"),
]
