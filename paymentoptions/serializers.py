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
            "interest_rate",
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

    def validate(self, attrs):
        payment_type = attrs.get("payment_type")
        min_deposit = attrs.get("min_deposit_percentage")

        if payment_type == "FLEXIBLE":
            if min_deposit is None:
                raise serializers.ValidationError(
                    {
                        "min_deposit_percentage": "This field is required for FLEXIBLE payment type."
                    }
                )
            if not (0 < min_deposit <= 100):
                raise serializers.ValidationError(
                    {"min_deposit_percentage": "Value must be between 0 and 100."}
                )
        return attrs
