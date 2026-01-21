from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth import get_user_model

from sublayeritems.models import SublayerItem
from sublayeritems.serializers import SublayerItemSerializer

User = get_user_model()


class SublayerItemListCreateView(generics.ListCreateAPIView):
    queryset = SublayerItem.objects.all().prefetch_related("brackets")
    serializer_class = SublayerItemSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SublayerItem.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SublayerItemListView(generics.ListAPIView):
    queryset = SublayerItem.objects.all().prefetch_related("brackets")
    serializer_class = SublayerItemSerializer
    permission_classes = [
        AllowAny,
    ]


class SublayerItemDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SublayerItem.objects.all().prefetch_related("brackets")
    serializer_class = SublayerItemSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"
