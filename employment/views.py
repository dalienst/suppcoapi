from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response

from accounts.models import User
from companies.permissions import IsOwnerOrReadOnly
from employment.models import Employment
from employment.serializers import EmploymentSerializer
from sites.models import Site
from branches.models import Branch
from employment.serializers import EmployeeAssignSerializer, EmployeeUnassignSerializer

User = get_user_model()


class EmploymentListView(generics.ListAPIView):
    queryset = Employment.objects.all()
    serializer_class = EmploymentSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EmployeeAssignView(generics.CreateAPIView):
    serializer_class = EmployeeAssignSerializer
    permission_classes = [IsOwnerOrReadOnly]


class EmployeeUnassignView(generics.GenericAPIView):
    serializer_class = EmployeeUnassignSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message": "Assignment removed."}, status=status.HTTP_200_OK)
