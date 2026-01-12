from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from inventory.models import Inventory
from companies.models import Company
from layers.serializers import LayerSerializer


class InventorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=800, required=True)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )
    user = serializers.CharField(source="user.username", read_only=True)
    layers = LayerSerializer(many=True, read_only=True)
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = (
            "id",
            "user",
            "company",
            "name",
            "inventory_code",
            "description",
            "created_at",
            "updated_at",
            "reference",
            "user_details",
            "layers",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Inventory.objects.all(),
                fields=["company", "name"],
                message="Inventory with this name already exists in this company.",
            )
        ]

    def get_user_details(self, obj):
        return {
            "username": obj.user.username,
            "email": obj.user.email,
            "reference": obj.user.reference,
            "account_type": obj.user.account_type,
        }
