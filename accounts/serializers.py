from django.contrib.auth import get_user_model
from django.utils import timezone
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from accounts.tokens import account_activation_token
from companies.models import Company
from accounts.utils import send_activation_email, send_employee_added_email
from accounts.validators import (
    validate_password_digit,
    validate_password_lowercase,
    validate_password_symbol,
    validate_password_uppercase,
)
from verification.models import VerificationCode
from companies.serializers import CompanySerializer
from companies.models import Company
from roles.models import Role
from branches.models import Branch
from sites.models import Site
from employment.models import Employment
from employment.serializers import EmploymentSerializer

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
    employment = EmploymentSerializer(many=True, read_only=True)

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
            "is_staff",
            "is_active",
            "is_contractor",
            "is_supplier",
            "is_employee",
            "assigned_site",
            "assigned_branch",
            "account_type",
            "created_at",
            "updated_at",
            "employment",
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
        user.account_type = "SUPPLIER"
        user.save()
        Company.objects.create(user=user, name=user.username)
        return user


class ContractorSerializer(BaseUserSerializer):
    def create(self, validated_data):
        user = self.create_user(validated_data, "is_contractor")
        user.account_type = "CONTRACTOR"
        user.save()
        Company.objects.create(user=user, name=user.username)
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


"""
Specified serializers for user details and listing
"""


class OwnerSerializer(BaseUserSerializer):
    company = CompanySerializer(read_only=True)

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
            "is_staff",
            "is_active",
            "is_contractor",
            "is_supplier",
            "assigned_site",
            "assigned_branch",
            "created_at",
            "updated_at",
            "account_type",
            "company",
            "employment",
        )


"""
Employees Serializers: invitations etc
"""


class EmployeeCreatedByOwnerSerializer(BaseUserSerializer):
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="identity", write_only=True
    )
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(), slug_field="identity", write_only=True
    )
    site = serializers.SlugRelatedField(
        queryset=Site.objects.all(),
        slug_field="identity",
        required=False,
        write_only=True,
    )
    branch = serializers.SlugRelatedField(
        queryset=Branch.objects.all(),
        slug_field="identity",
        required=False,
        write_only=True,
    )
    employment = EmploymentSerializer(many=True, read_only=True)

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
            "is_staff",
            "is_active",
            "is_contractor",
            "is_supplier",
            "assigned_site",
            "assigned_branch",
            "created_at",
            "updated_at",
            "account_type",
            "company",
            "role",
            "site",
            "branch",
            "employment",
        )

    def validate(self, attrs):
        company = attrs.get("company")
        role = attrs.get("role")
        site = attrs.get("site", None)
        branch = attrs.get("branch", None)

        # Check if user is owner of the company
        if not self.context["request"].user == company.user:
            raise serializers.ValidationError(
                "You must be the company owner to create an employee."
            )

        if role.company != company:
            raise serializers.ValidationError("Role is not in this company")

        # Prevent assigning both site and branch
        if site and branch:
            raise serializers.ValidationError("Cannot assign both site and branch")

        if site and site.company != company:
            raise serializers.ValidationError("Site is not in this company")
        if branch and branch.company != company:
            raise serializers.ValidationError("Branch is not in this company")

        return attrs

    def create(self, validated_data):
        company = validated_data.pop("company")
        role = validated_data.pop("role")
        site = validated_data.pop("site", None)
        branch = validated_data.pop("branch", None)
        temporary_password = validated_data.get("password")

        # Create User
        user = self.create_user(validated_data, "is_employee")
        user.account_type = "EMPLOYEE"
        user.save()

        # Create Employment
        Employment.objects.create(user=user, company=company, role=role)

        # Handle site/branch assignment
        if site:
            user.assigned_site = site
            if role.is_head:
                site.head = user
                site.save()
            user.save()
        elif branch:
            user.assigned_branch = branch
            if role.is_head:
                branch.head = user
                branch.save()
            user.save()

        # Send employee added email with credentials
        send_employee_added_email(
            self.context["request"].user, user, temporary_password
        )

        return user
