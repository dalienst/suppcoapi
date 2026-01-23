from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from paymentplans.models import PaymentPlan
from paymentplans.serializers import PaymentPlanSerializer


class PaymentPlanListCreateView(generics.ListCreateAPIView):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return PaymentPlan.objects.filter(user=self.request.user)


class PaymentPlanRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = PaymentPlan.objects.all()
    serializer_class = PaymentPlanSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        return PaymentPlan.objects.filter(user=self.request.user)
