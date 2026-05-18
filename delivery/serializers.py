from rest_framework import serializers
from .models import DeliveryZone
from companies.serializers import CompanySerializer


class DeliveryZoneSerializer(serializers.ModelSerializer):
    company_details = CompanySerializer(source="company", read_only=True)

    class Meta:
        model = DeliveryZone
        fields = (
            "id",
            "reference",
            "company",
            "company_details",
            "city",
            "fee",
            "estimated_days",
            "is_active",
            "created_at",
            "updated_at",
        )
        read_only_fields = ("id", "reference", "created_at", "updated_at")

    def validate_fee(self, value):
        if value < 0:
            raise serializers.ValidationError("Delivery fee cannot be negative.")
        return value
