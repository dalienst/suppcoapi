from django.contrib.auth import authenticate, get_user_model
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status
from rest_framework.authtoken.models import Token
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from accounts.serializers import (
    BaseUserSerializer,
    ContractorSerializer,
    SupplierSerializer,
    VerifyAccountSerializer,
    UserLoginSerializer,
    RequestPasswordResetSerializer,
    PasswordResetSerializer,
)
from accounts.utils import send_password_reset_email

User = get_user_model()

"""
Login and Logout Views
"""


class LoginView(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserLoginSerializer

    def post(self, request, format=None):

        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            email = serializer.validated_data["email"]
            password = serializer.validated_data["password"]
            user = authenticate(email=email, password=password)

            if user:
                if user.is_active:
                    token, created = Token.objects.get_or_create(user=user)
                    user_details = {
                        "id": user.id,
                        "email": user.email,
                        "username": user.username,
                        "is_superuser": user.is_superuser,
                        "is_active": user.is_active,
                        "is_staff": user.is_staff,
                        "is_contractor": user.is_contractor,
                        "is_supplier": user.is_supplier,
                        "is_subcontractor": user.is_subcontractor,
                        "reference": user.reference,
                        "slug": user.slug,
                        "last_login": user.last_login,
                        "token": token.key,
                    }
                    return Response(user_details, status=status.HTTP_200_OK)
                else:
                    return Response(
                        {"detail": ("User account is disabled.")},
                        status=status.HTTP_400_BAD_REQUEST,
                    )
            else:
                return Response(
                    {"detail": ("Unable to log in with provided credentials.")},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


"""
Suppliers, Contractors Views
"""


class SupplierCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SupplierSerializer
    permission_classes = (AllowAny,)


class ContractorCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = ContractorSerializer
    permission_classes = (AllowAny,)


"""
User Profile Views
"""


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = BaseUserSerializer
    queryset = User.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return super().get_queryset().filter(id=self.request.user.id)


"""
Account Verification
"""


class VerifyAccountView(GenericAPIView):
    serializer_class = VerifyAccountSerializer

    def patch(self, request, uidb64, token, **kwargs):
        data = {"uidb64": uidb64, "token": token}
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(
            {
                "message": "Email activated successfully",
            },
            status=status.HTTP_200_OK,
        )


"""
Public Views
"""


class UsersListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = (AllowAny,)


class UserPublicProfile(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = BaseUserSerializer
    permission_classes = (AllowAny,)
    lookup_field = "username"


"""
Password Reset
"""


class RequestPasswordResetView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = RequestPasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            verification = serializer.save()

            send_password_reset_email(verification.user, verification.code)

            return Response(
                {"message": "Password reset email sent successfully!"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                {"message": "Password reset successful!"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
