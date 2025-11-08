from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from companies.permissions import IsSupplierOrReadOnly
from branches.models import Branch
from branches.serializers import BranchSerializer


class BranchListCreateView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [
        IsAuthenticated,
        IsSupplierOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [
        IsAuthenticated,
        IsSupplierOrReadOnly,
    ]
    lookup_field = "identity"
