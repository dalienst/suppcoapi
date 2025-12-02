from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from sublayeritems.models import SublayerItem
from sublayeritems.serializers import SublayerItemSerializer


class SublayerItemListView(generics.ListCreateAPIView):
    queryset = SublayerItem.objects.all()
    serializer_class = SublayerItemSerializer
    permission_classes = [IsAuthenticated]


class SublayerItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SublayerItem.objects.all()
    serializer_class = SublayerItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"
