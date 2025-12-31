from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from sublayers.models import SubLayer
from sublayers.serializers import SubLayerSerializer


class SubLayerListCreateView(generics.ListCreateAPIView):
    queryset = SubLayer.objects.all().prefetch_related("sublayeritems")
    serializer_class = SubLayerSerializer
    permission_classes = [IsAuthenticated]


class SubLayerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubLayer.objects.all().prefetch_related("sublayeritems")
    serializer_class = SubLayerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"
    