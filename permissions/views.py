from rest_framework import generics
from rest_framework.permissions import IsAdminUser

from permissions.models import Permission
from permissions.serializers import PermissionSerializer


class PermissionListCreateView(generics.ListCreateAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [
        IsAdminUser,
    ]


class PermissionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Permission.objects.all()
    serializer_class = PermissionSerializer
    permission_classes = [
        IsAdminUser,
    ]
    lookup_field = ("reference",)
