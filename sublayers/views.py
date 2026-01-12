from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from sublayers.models import SubLayer
from sublayers.serializers import SubLayerSerializer


class SubLayerListView(generics.ListAPIView):
    queryset = SubLayer.objects.all().prefetch_related("sublayeritems")
    serializer_class = SubLayerSerializer
    permission_classes = [
        AllowAny,
    ]


class SubLayerListCreateView(generics.ListCreateAPIView):
    queryset = SubLayer.objects.all().prefetch_related("sublayeritems")
    serializer_class = SubLayerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubLayer.objects.filter(user=self.request.user)


class SubLayerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubLayer.objects.all().prefetch_related("sublayeritems")
    serializer_class = SubLayerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"
