from rest_framework import generics
from rest_framework.permissions import IsAuthenticated


from brackets.models import Bracket
from brackets.serializers import BracketSerializer


class BracketListCreateView(generics.ListCreateAPIView):
    queryset = Bracket.objects.all()
    serializer_class = BracketSerializer
    permission_classes = [IsAuthenticated]


class BracketRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Bracket.objects.all()
    serializer_class = BracketSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = "reference"
