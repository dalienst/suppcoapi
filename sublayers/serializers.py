from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from sublayers.models import SubLayer
from layers.models import Layer


class SubLayerSerializer(serializers.ModelSerializer):
    layer = serializers.SlugRelatedField(
        queryset=Layer.objects.all(), slug_field="name"
    )
    name = serializers.CharField()

    class Meta:
        model = SubLayer
        fields = (
            "name",
            "layer",
            "created_at",
            "updated_at",
            "reference",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=SubLayer.objects.all(),
                fields=["layer", "name"],
                message="SubLayer with this name already exists in this layer.",
            )
        ]
