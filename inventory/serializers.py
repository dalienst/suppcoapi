from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from inventory.models import Inventory
from companies.models import Company


class InventorySerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=800, required=True)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )
    user = serializers.CharField(source="user.username", read_only=True)

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
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Inventory.objects.all(),
                fields=["company", "name"],
                message="Inventory with this name already exists in this company.",
            )
        ]
