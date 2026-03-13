from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from companies.permissions import IsSupplierOrReadOnly
from branches.models import Branch
from branches.serializers import BranchSerializer


class BranchListCreateView(generics.ListCreateAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [
        IsSupplierOrReadOnly,
    ]

    # if he is supplier, return all branches of that supplier
    def get_queryset(self):
        if self.request.user.is_supplier:
            return Branch.objects.filter(company=self.request.user.company)
        return Branch.objects.all()


class BranchDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Branch.objects.all()
    serializer_class = BranchSerializer
    permission_classes = [
        IsSupplierOrReadOnly,
    ]
    lookup_field = "identity"

    # if he is supplier, return all branches of that supplier
    def get_queryset(self):
        if self.request.user.is_supplier:
            return Branch.objects.filter(company=self.request.user.company)
        return Branch.objects.all()
