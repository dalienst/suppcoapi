from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from layers.models import Layer
from layers.serializers import LayerSerializer


class LayerListView(generics.ListAPIView):
    queryset = Layer.objects.all().prefetch_related("sublayers")
    serializer_class = LayerSerializer
    permission_classes = [
        AllowAny,
    ]

    def get_queryset(self):
        if self.request.user.is_authenticated:
            if self.request.user.is_supplier or self.request.user.is_contractor:
                return Layer.objects.filter(inventory__company=self.request.user.company)
            return Layer.objects.filter(user=self.request.user)
        return Layer.objects.all()


class LayerListCreateView(generics.ListCreateAPIView):
    queryset = Layer.objects.all().prefetch_related("sublayers")
    serializer_class = LayerSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Layer.objects.filter(user=self.request.user)


class LayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Layer.objects.all().prefetch_related("sublayers")
    serializer_class = LayerSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "reference"
