from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.tokens import account_activation_token
from companies.models import Company
from accounts.utils import send_activation_email
from accounts.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)
from verification.models import VerificationCode

User = get_user_model()


class BaseUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())],
    )
    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )
    avatar = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = User
        fields = (
            "id",
            "email",
            "username",
            "password",
            "first_name",
            "last_name",
            "avatar",
            "phone",
            "identification",
            "kra_pin",
            "location",
            "reference",
            "created_at",
            "updated_at",
            "is_staff",
            "is_active",
            "is_contractor",
            "is_supplier",
            "is_subcontractor",
        )

    def create_user(self, validated_data, role_field):
        user = User.objects.create_user(**validated_data)
        setattr(user, role_field, True)
        user.save()
        send_activation_email(user)
        return user


class SupplierSerializer(BaseUserSerializer):
    def create(self, validated_data):
        user = self.create_user(validated_data, "is_supplier")
        user.save()
        Company.objects.create(user=user)
        return user


class ContractorSerializer(BaseUserSerializer):
    def create(self, validated_data):
        user = self.create_user(validated_data, "is_contractor")
        user.save()
        Company.objects.create(user=user)
        return user


class VerifyAccountSerializer(serializers.Serializer):
    uidb64 = serializers.CharField()
    token = serializers.CharField()

    class Meta:
        fields = ("uidb64", "token")

    def validate(self, data):
        user = None
        try:
            user_id = force_str(urlsafe_base64_decode(data.get("uidb64")))
            user = User.objects.get(id=user_id)

        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            raise serializers.ValidationError("Invalid user id", code="invalid_code")

        token = data.get("token")
        if user and not account_activation_token.check_token(user, token):
            raise serializers.ValidationError("Invalid token", code="invalid_token")

        return data

    def save(self, **kwargs):
        user_id = force_str(urlsafe_base64_decode(self.validated_data.get("uidb64")))
        user = User.objects.get(id=user_id)
        user.is_active = True
        user.save()
        return user


class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(required=True, write_only=True)

"""
Password Reset Serializers
"""


class RequestPasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Account with this email does not exist!")
        return email

    def save(self):
        email = self.validated_data.get("email")
        user = User.objects.get(email=email)

        # create verification code
        verification = VerificationCode.objects.create(
            user=user, purpose="password_reset"
        )

        return verification


class PasswordResetSerializer(serializers.Serializer):
    code = serializers.CharField()
    password = serializers.CharField(
        max_length=128,
        min_length=5,
        write_only=True,
        validators=[
            validate_password_digit,
            validate_password_uppercase,
            validate_password_symbol,
            validate_password_lowercase,
        ],
    )

    def validate(self, attrs):
        code = attrs.get("code")

        try:
            verification = VerificationCode.objects.get(
                code=code, purpose="password_reset", used=False
            )
        except VerificationCode.DoesNotExist:
            raise serializers.ValidationError("Invalid or expired verification code!")

        if not verification.is_valid():
            raise serializers.ValidationError(
                "The code has expired or already been used!"
            )

        attrs["verification"] = verification
        attrs["user"] = verification.user
        return attrs

    def save(self):
        user = self.validated_data.get("user")
        verification = self.validated_data.get("verification")
        password = self.validated_data.get("password")

        # update password
        user.set_password(password)
        user.save()

        # mark code as used
        verification.used = True
        verification.save()

        return user
