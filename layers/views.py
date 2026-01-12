from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from layers.models import Layer
from layers.serializers import LayerSerializer


class LayerListView(generics.ListAPIView):
    queryset = Layer.objects.all().prefetch_related("sublayers")
    serializer_class = LayerSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class LayerListCreateView(generics.ListCreateAPIView):
    queryset = Layer.objects.all().prefetch_related("sublayers")
    serializer_class = LayerSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def get_queryset(self):
        return Layer.objects.filter(inventory__user=self.request.user)


class LayerDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Layer.objects.all().prefetch_related("sublayers")
    serializer_class = LayerSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "reference"
