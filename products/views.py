from rest_framework import generics

from products.models import Product
from products.serializers import ProductSerializer
from companies.permissions import IsOwnerOrReadOnly


class ProductListCreateView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [ IsOwnerOrReadOnly]
    filterset_fields = ["layer", "sublayer", "sublayeritem", "bracket", "company"]
    search_fields = ["product_name", "sku"]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # return only the products in that company for suppliers, all for contractors
    def get_queryset(self):
        if self.request.user.is_supplier:
            return Product.objects.filter(company=self.request.user.company)
        return Product.objects.all()


class ProductDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly]
    lookup_field = "reference"

    # return only the products in that company
    def get_queryset(self):
        if self.request.user.is_supplier or self.request.user.is_contractor:
            return Product.objects.filter(company=self.request.user.company)
        return Product.objects.all()
