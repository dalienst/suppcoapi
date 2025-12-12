# roles/serializers.py

from rest_framework import serializers
from django.shortcuts import get_object_or_404

from roles.models import Role
from companies.models import Company
from permissions.models import Permission


class RoleSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.SlugRelatedField(
        slug_field="identity",
        queryset=Company.objects.all(),
        required=False,  # Important for PATCH
        allow_null=True,
    )
    permissions = serializers.SlugRelatedField(
        slug_field="codename",
        queryset=Permission.objects.all(),
        many=True,
        required=False,
    )
    permissions_details = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Role
        fields = (
            "id",
            "user",
            "name",
            "is_head",
            "company",
            "identity",
            "permissions",
            "permissions_details",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("user", "identity", "created_at", "updated_at")

    def validate(self, attrs):
        request = self.context["request"]
        user = request.user

        # On CREATE: company is provided (creation)
        company = attrs.get("company")

        # On UPDATE: company might not be in payload → get from instance
        if not company and self.instance:
            company = self.instance.company

        # Now safe to check ownership
        if company and company.user != user:
            raise serializers.ValidationError(
                "You can only manage roles for your own company."
            )

        # Prevent duplicate role name (case-insensitive) in the same company
        name = attrs.get("name", self.instance.name if self.instance else None)
        if name and company:
            queryset = Role.objects.filter(company=company, name__iexact=name)
            if self.instance:
                queryset = queryset.exclude(pk=self.instance.pk)
            if queryset.exists():
                raise serializers.ValidationError(
                    "A role with this name already exists in your company."
                )

        return attrs

    def create(self, validated_data):
        permissions = validated_data.pop("permissions", [])
        role = Role.objects.create(**validated_data)
        if permissions:
            role.permissions.set(permissions)
        return role

    def update(self, instance, validated_data):
        permissions = validated_data.pop("permissions", None)

        # Update fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Update permissions if provided
        if permissions is not None:
            instance.permissions.set(permissions)

        return instance

    def get_permissions_details(self, obj):
        return [
            {
                "name": p.name,
                "codename": p.codename,
                "description": p.description or "",
            }
            for p in obj.permissions.all()
        ]
