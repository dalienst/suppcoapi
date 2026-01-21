from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny


from brackets.models import Bracket
from brackets.serializers import BracketSerializer


class BracketListView(generics.ListAPIView):
    queryset = Bracket.objects.all()
    serializer_class = BracketSerializer
    permission_classes = [
        AllowAny,
    ]


class BracketListCreateView(generics.ListCreateAPIView):
    queryset = Bracket.objects.all()
    serializer_class = BracketSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        return Bracket.objects.filter(user=self.request.user)


class BracketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bracket.objects.all()
    serializer_class = BracketSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"
