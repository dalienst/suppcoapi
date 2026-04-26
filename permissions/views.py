from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from permissions.models import Permission
from permissions.serializers import PermissionSerializer


class PermissionListCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [
        IsAuthenticated,
    ]


class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [
        IsAuthenticated,
    ]
    lookup_field = ("reference",)
