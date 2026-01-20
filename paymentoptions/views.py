from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from paymentoptions.models import PaymentOption
from paymentoptions.serializers import PaymentOptionSerializer


class PaymentOptionListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PaymentOptionSerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return PaymentOption.objects.filter(user=self.request.user)


class PaymentOptionRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PaymentOptionSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "reference"

    def get_queryset(self):
        return PaymentOption.objects.filter(user=self.request.user)
