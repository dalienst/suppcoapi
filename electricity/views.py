from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from electricity.models import Electricity
from electricity.serializers import ElectricitySerializer


class ElectricityListCreateView(generics.ListCreateAPIView):
    queryset = Electricity.objects.all()
    serializer_class = ElectricitySerializer
    permission_classes = [
        IsAuthenticated,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Electricity.objects.filter(user=self.request.user)


class ElectricityRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Electricity.objects.all()
    serializer_class = ElectricitySerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = "reference"

    def get_object(self):
        return Electricity.objects.get(user=self.request.user)


class ElectricityListView(generics.ListAPIView):
    queryset = Electricity.objects.all()
    serializer_class = ElectricitySerializer
    permission_classes = [
        AllowAny,
    ]
