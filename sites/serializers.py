from rest_framework import serializers
from django.contrib.auth import get_user_model

from sites.models import Site
from companies.models import Company

User = get_user_model()


class SiteProductMiniSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source="product_name", read_only=True)

    class Meta:
        from products.models import Product
        model = Product
        fields = ("reference", "name", "sku", "quantity")

class SiteStaffMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("username", "email", "first_name", "last_name", "account_type")

class SiteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.CharField(source="user.company.name", read_only=True)
    head = serializers.CharField(source="head.username", read_only=True)
    head_details = SiteStaffMiniSerializer(source="head", read_only=True)
    assigned_staff = SiteStaffMiniSerializer(many=True, read_only=True)
    site_products = SiteProductMiniSerializer(many=True, read_only=True)

    class Meta:
        model = Site
        fields = (
            "id",
            "user",
            "name",
            "company",
            "head",
            "head_details",
            "address",
            "reference",
            "identity",
            "assigned_staff",
            "site_products",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            company = user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("You are not a company owner")

        return Site.objects.create(user=user, company=company, **validated_data)
