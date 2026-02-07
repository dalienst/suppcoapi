from django.urls import path

from cart.views import CartDetailView

app_name = "cart"

urlpatterns = [
    path("<str:user__username>/", CartDetailView.as_view(), name="cart-detail"),
]
