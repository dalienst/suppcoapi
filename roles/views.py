from rest_framework import generics

from roles.models import Role
from roles.serializers import RoleSerializer
from companies.permissions import IsOwnerOrReadOnly


class RoleListCreateView(generics.ListCreateAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
    ]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    # TODO: only get roles for the company that the user is in either as the owner or staff
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class RoleDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer
    permission_classes = [
        IsOwnerOrReadOnly,
    ]
    lookup_field = "identity"

    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
