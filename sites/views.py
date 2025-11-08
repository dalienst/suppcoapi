from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from sites.models import Site
from sites.serializers import SiteSerializer
from companies.permissions import IsContractorOrReadOnly


class SiteListCreateView(generics.ListCreateAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [
        IsContractorOrReadOnly,
    ]


class SiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [
        IsContractorOrReadOnly,
    ]
    lookup_field = "identity"
