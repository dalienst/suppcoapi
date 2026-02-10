from rest_framework import generics, permissions
from django.db.models import Q
from orders.models import Order
from .serializers import SupplierOrderSerializer


class SupplierOrderListCreateView(generics.ListCreateAPIView):
    serializer_class = SupplierOrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        # Retrieve orders where the user's company is the supplier
        # User can be owner (user.company) or employee (user.employees -> company)
        # Note: 'user.employees' related name on Company.staff is distinct from 'user.company'

        # 1. Owned Company
        # defined in Company model: user = OneToOneField(..., related_name="company")
        # So user.company is the Company object.

        # 2. Employer Company
        # defined in Company model: staff = ManyToMany(..., related_name="employees")
        # So user.employees.all() returns list of companies they work for.

        try:
            owned_company = user.company
        except Exception:
            owned_company = None

        employer_companies = user.employees.all()

        # Filter Orders where company matches
        return Order.objects.filter(
            Q(company=owned_company) | Q(company__in=employer_companies)
        ).distinct()

    def perform_create(self, serializer):
        # Suppliers generally don't create orders here, but if necessary:
        serializer.save(user=self.request.user)


class SupplierOrderRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = SupplierOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        user = self.request.user
        try:
            owned_company = user.company
        except Exception:
            owned_company = None

        employer_companies = user.employees.all()

        return Order.objects.filter(
            Q(company=owned_company) | Q(company__in=employer_companies)
        ).distinct()
