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

    # if he is contractor, return all sites of that contractor
    def get_queryset(self):
        if self.request.user.is_contractor:
            return Site.objects.filter(company=self.request.user.company)
        return Site.objects.all()


class SiteDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Site.objects.all()
    serializer_class = SiteSerializer
    permission_classes = [
        IsContractorOrReadOnly,
    ]
    lookup_field = "identity"

    # if he is contractor, return all sites of that contractor
    def get_queryset(self):
        if self.request.user.is_contractor:
            return Site.objects.filter(company=self.request.user.company)
        return Site.objects.all()
