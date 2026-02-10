from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cartitems.models import CartItem
from cartitems.serializers import CartItemSerializer


class CartItemListView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)


class CartItemDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = CartItem.objects.all()
    serializer_class = CartItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        return CartItem.objects.filter(cart__user=self.request.user)

    # if quantity is 0 or less than 0 delete the cart item and remove it from the cart
    def perform_update(self, serializer):
        if serializer.validated_data["quantity"] <= 0:
            serializer.instance.delete()
        else:
            serializer.save()
