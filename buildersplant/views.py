from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny

from buildersplant.models import BuilderPlant
from buildersplant.serializers import BuilderPlantSerializer


class BuilderPlantListCreateView(generics.ListCreateAPIView):
    queryset = BuilderPlant.objects.all()
    serializer_class = BuilderPlantSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return BuilderPlant.objects.filter(user=self.request.user)


class BuilderPlantRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = BuilderPlant.objects.all()
    serializer_class = BuilderPlantSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"

    def get_queryset(self):
        return BuilderPlant.objects.filter(user=self.request.user)


class BuilderPlantListView(generics.ListAPIView):
    queryset = BuilderPlant.objects.all()
    serializer_class = BuilderPlantSerializer
    permission_classes = [AllowAny]
