from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from layers.models import Layer
from inventory.models import Inventory
from sublayers.serializers import SubLayerSerializer


class LayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
    )
    inventory = serializers.SlugRelatedField(
        slug_field="inventory_code", queryset=Inventory.objects.all()
    )
    sublayers = SubLayerSerializer(many=True, read_only=True)
    inventory_details = serializers.SerializerMethodField()

    class Meta:
        model = Layer
        fields = (
            "name",
            "inventory",
            "created_at",
            "updated_at",
            "reference",
            "inventory_details",
            "sublayers",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Layer.objects.all(),
                fields=["inventory", "name"],
                message="Layer with this name already exists in this inventory.",
            )
        ]

    def get_inventory_details(self, obj):
        return {
            "inventory_code": obj.inventory.inventory_code,
            "name": obj.inventory.name,
            "company": {
                "name": obj.inventory.company.name,
            },
        }
