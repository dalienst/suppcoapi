from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from layers.models import Layer
from inventory.models import Inventory


class LayerSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=255,
        validators=[UniqueValidator(queryset=Layer.objects.all())],
    )
    inventory = serializers.SlugRelatedField(
        slug_field="inventory_code", queryset=Inventory.objects.all()
    )

    class Meta:
        model = Layer
        fields = (
            "name",
            "inventory",
            "created_at",
            "updated_at",
            "reference",
        )
