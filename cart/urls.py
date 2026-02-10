from django.urls import path

from cart.views import CartDetailView

app_name = "cart"

urlpatterns = [
    path("", CartDetailView.as_view(), name="cart-detail"),
]
