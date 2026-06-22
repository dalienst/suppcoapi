from rest_framework import generics, permissions, serializers
from .models import DeliveryZone
from .serializers import DeliveryZoneSerializer


class DeliveryZoneListCreateView(generics.ListCreateAPIView):
    serializer_class = DeliveryZoneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = DeliveryZone.objects.filter(is_active=True)
        company_reference = self.request.query_params.get("company")
        if company_reference:
            queryset = queryset.filter(company__reference=company_reference)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        try:
            company = user.company
        except Exception:
            company = user.employees.first()

        if not company:
            raise serializers.ValidationError("You must be associated with a registered Supplier Company to create delivery zones.")
        
        serializer.save(company=company)


class DeliveryZoneRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = DeliveryZone.objects.all()
    serializer_class = DeliveryZoneSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    lookup_field = "reference"
