from rest_framework import serializers
from .models import OrderDelivery
from delivery.serializers import DeliveryZoneSerializer


class OrderDeliverySerializer(serializers.ModelSerializer):
    delivery_zone_details = DeliveryZoneSerializer(source="delivery_zone", read_only=True)
    order_reference = serializers.ReadOnlyField(source="order.reference")

    class Meta:
        model = OrderDelivery
        fields = (
            "id",
            "reference",
            "order",
            "order_reference",
            "delivery_method",
            "delivery_zone",
            "delivery_zone_details",
            "shipping_fee",
            "delivery_address",
            "recipient_name",
            "recipient_phone",
            "status",
            "secure_pin",
            "carrier_name",
            "tracking_number",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "reference",
            "secure_pin",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        delivery_method = attrs.get("delivery_method")
        delivery_zone = attrs.get("delivery_zone")

        if delivery_method == "DELIVERY" and not delivery_zone and not attrs.get("delivery_address"):
            raise serializers.ValidationError(
                "A delivery zone and delivery address are required when delivery method is set to Supplier Managed Delivery."
            )
        return attrs
