from rest_framework import serializers
from django.contrib.auth import get_user_model

from paymentoptions.models import PaymentOption

User = get_user_model()


class PaymentOptionSerializer(serializers.ModelSerializer):
    user = serializers.CharField(read_only=True, source="user.username")
    is_active = serializers.BooleanField(default=True)

    class Meta:
        model = PaymentOption
        fields = [
            "payment_type",
            "min_deposit_percentage",
            "name",
            "description",
            "is_active",
            "is_fixed",
            "is_payment_on_delivery",
            "is_split_50_50",
            "is_flexible",
            "created_at",
            "updated_at",
            "reference",
            "user",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "reference",
            "is_fixed",
            "is_payment_on_delivery",
            "is_split_50_50",
            "is_flexible",
            "user",
        ]
