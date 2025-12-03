from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from plumbing.models import Plumbing
from plumbing.serializers import PlumbingSerializer


class PlumbingListCreateView(generics.ListCreateAPIView):
    queryset = Plumbing.objects.all()
    serializer_class = PlumbingSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Plumbing.objects.filter(user=self.request.user)


class PlumbingRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Plumbing.objects.all()
    serializer_class = PlumbingSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "reference"

    def get_object(self):
        return Plumbing.objects.get(user=self.request.user)


class PlumbingListView(generics.ListAPIView):
    queryset = Plumbing.objects.all()
    serializer_class = PlumbingSerializer
    permission_classes = [
        AllowAny,
    ]
