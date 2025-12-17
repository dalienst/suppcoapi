from django.urls import path

from products.views import ProductDetailView, ProductListCreateView

app_name = "products"

urlpatterns = [
    path("", ProductListCreateView.as_view(), name="products-list-create"),
    path("<str:reference>/", ProductDetailView.as_view(), name="products-detail"),
]
