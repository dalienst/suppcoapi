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
    filterset_fields = ["layer", "layer__reference"]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_supplier or self.request.user.is_contractor:
                return SubLayer.objects.filter(layer__inventory__company=self.request.user.company)
            return SubLayer.objects.filter(user=self.request.user)
        return SubLayer.objects.all()


class SubLayerListCreateView(generics.ListCreateAPIView):
    queryset = SubLayer.objects.all().prefetch_related("sublayeritems")
    serializer_class = SubLayerSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SubLayer.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SubLayerRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SubLayer.objects.all().prefetch_related("sublayeritems")
    serializer_class = SubLayerSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"
