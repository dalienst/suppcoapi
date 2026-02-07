from django.urls import path

from cartitems.views import CartItemListView, CartItemDetailViewSet

urlpatterns = [
    path("", CartItemListView.as_view(), name="cartitems"),
    path("<str:reference>/", CartItemDetailViewSet.as_view(), name="cartitem"),
]
