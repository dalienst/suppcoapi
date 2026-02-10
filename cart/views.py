from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from cart.models import Cart
from cart.serializers import CartSerializer
from cartitems.models import CartItem


class CartDetailView(generics.RetrieveUpdateAPIView):
    """
    Get the cart of the authenticated user
    Update the cart of the authenticated user - clear all items and add new items
    """

    queryset = Cart.objects.all()
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def get_object(self):
        return self.get_queryset().get(user=self.request.user)

    def update(self, instance, validated_data):
        instance.items.all().delete()
        for item in validated_data["items"]:
            CartItem.objects.create(cart=instance, **item)
        return instance
