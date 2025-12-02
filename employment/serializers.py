from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404

from employment.models import Employment
from roles.models import Role
from companies.models import Company
from branches.models import Branch
from sites.models import Site

User = get_user_model()


class EmploymentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(), slug_field="identity"
    )
    user_detail = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = Employment
        fields = (
            "user",
            "user_detail",
            "company",
            "role",
            "is_active",
            "identity",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        company = attrs.get("company")
        role = attrs.get("role")
        if role.company != company:
            raise serializers.ValidationError("Role is not in this company")
        return attrs


class EmployeeAssignSerializer(serializers.Serializer):
    employee_username = serializers.CharField(write_only=True)
    site = serializers.CharField(required=False, write_only=True)
    branch = serializers.CharField(required=False, write_only=True)

    def validate(self, data):
        username = data["employee_username"]
        site_identity = data.get("site")
        branch_identity = data.get("branch")
        request = self.context["request"]

        # Must provide exactly one location
        if site_identity and branch_identity:
            raise serializers.ValidationError("Cannot assign to both site and branch.")
        if not site_identity and not branch_identity:
            raise serializers.ValidationError("Must provide either 'site' or 'branch'.")

        # Find employee by username
        try:
            employee = User.objects.get(username=username)
        except User.DoesNotExist:
            raise serializers.ValidationError("Employee with this username not found.")

        # Must be an active employee of the owner's company
        owner_company = request.user.company
        try:
            employment = Employment.objects.get(
                user=employee, company=owner_company, is_active=True
            )
        except Employment.DoesNotExist:
            raise serializers.ValidationError(
                "This employee does not work for your company."
            )

        # Site (Contractors only)
        if site_identity:
            if not request.user.is_contractor:
                raise serializers.ValidationError(
                    "Only contractors can assign to sites."
                )
            location = get_object_or_404(
                Site, identity=site_identity, company=owner_company
            )
            location_type = "site"
        else:
            if not request.user.is_supplier:
                raise serializers.ValidationError(
                    "Only suppliers can assign to branches."
                )
            location = get_object_or_404(
                Branch, identity=branch_identity, company=owner_company
            )
            location_type = "branch"

        data["employee"] = employee
        data["employment"] = employment
        data["location"] = location
        data["location_type"] = location_type
        return data

    def create(self, validated_data):
        employee = validated_data["employee"]
        employment = validated_data["employment"]
        location = validated_data["location"]
        location_type = validated_data["location_type"]

        # Clear the opposite assignment
        if location_type == "site":
            employee.assigned_site = location
            employee.assigned_branch = None
        else:
            employee.assigned_branch = location
            employee.assigned_site = None

        # Auto-assign as head if role allows
        if employment.role.is_head:
            location.head = employee
            location.save()

        employee.save()
        return employee

    def to_representation(self, instance):
        employment = self.validated_data["employment"]
        return {
            "employee_username": instance.username,
            "assigned_site": (
                instance.assigned_site.identity if instance.assigned_site else None
            ),
            "assigned_branch": (
                instance.assigned_branch.identity if instance.assigned_branch else None
            ),
            "is_head": employment.role.is_head,
            "message": "Employee assigned successfully.",
        }


class EmployeeUnassignSerializer(serializers.Serializer):
    employee_username = serializers.CharField()

    def validate_employee_username(self, value):
        try:
            employee = User.objects.get(username=value)
        except User.DoesNotExist:
            raise serializers.ValidationError("Employee not found.")

        request = self.context["request"]
        try:
            Employment.objects.get(
                user=employee, company=request.user.company, is_active=True
            )
        except Employment.DoesNotExist:
            raise serializers.ValidationError(
                "This employee does not work for your company."
            )

        return employee

    def save(self):
        employee = self.validated_data["employee_username"]
        employee.assigned_site = None
        employee.assigned_branch = None
        employee.save()
        return employee
