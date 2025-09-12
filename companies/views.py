from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from companies.models import Company
from companies.permissions import IsOwnerOrReadOnly
from companies.serializers import CompanySerializer


class CompanyDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticated,
        IsOwnerOrReadOnly,
    ]
    lookup_field = "identity"

    def get_queryset(self):
        return Company.objects.filter(user=self.request.user)


class CompanyListView(generics.ListAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [
        IsAuthenticated,
    ]


