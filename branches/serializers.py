from rest_framework import serializers
from django.contrib.auth import get_user_model

from branches.models import Branch
from companies.models import Company
from products.models import Product

User = get_user_model()


class BranchProductMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = (
            "id",
            "name",
            "sku",
            "reference",
            "created_at",
        )


class BranchStaffMiniSerializer(serializers.ModelSerializer):
    role_name = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            "id",
            "first_name",
            "last_name",
            "username",
            "email",
            "phone",
            "role_name",
        )

    def get_role_name(self, obj):
        employment = obj.employment.first() if hasattr(obj, "employment") else None
        if employment and employment.role:
            return employment.role.name
        return None


class BranchSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.CharField(source="user.company.name", read_only=True)
    head_details = BranchStaffMiniSerializer(source="head", read_only=True)
    assigned_staff = BranchStaffMiniSerializer(many=True, read_only=True)
    branch_products = BranchProductMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Branch
        fields = (
            "id",
            "user",
            "name",
            "company",
            "address",
            "reference",
            "identity",
            "head",
            "head_details",
            "assigned_staff",
            "branch_products",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            company = user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("You are not a company owner")

        return Branch.objects.create(user=user, company=company, **validated_data)
