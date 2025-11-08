from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from sites.models import Site
from sites.serializers import SiteSerializer
from companies.permissions import IsContractorOrReadOnly


class SiteListCreateView(generics.ListCreateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [IsContractorOrReadOnly, IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class SiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [
        IsContractorOrReadOnly,
        IsAuthenticated,
    ]
    lookup_field = "identity"
