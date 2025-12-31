from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from sublayers.models import SubLayer
from layers.models import Layer
from sublayeritems.serializers import SublayerItemSerializer


class SubLayerSerializer(serializers.ModelSerializer):
    layer = serializers.SlugRelatedField(
        queryset=Layer.objects.all(), slug_field="reference"
    )
    name = serializers.CharField()
    sublayeritems = SublayerItemSerializer(many=True, read_only=True)

    class Meta:
        model = SubLayer
        fields = (
            "name",
            "layer",
            "created_at",
            "updated_at",
            "reference",
            "sublayeritems",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=SubLayer.objects.all(),
                fields=["layer", "name"],
                message="SubLayer with this name already exists in this layer.",
            )
        ]
