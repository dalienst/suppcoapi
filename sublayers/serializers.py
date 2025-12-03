from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from sublayers.models import SubLayer
from layers.models import Layer


class SubLayerSerializer(serializers.ModelSerializer):
    layer = serializers.SlugRelatedField(
        queryset=Layer.objects.all(), slug_field="name"
    )
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=SubLayer.objects.all())]
    )

    class Meta:
        model = SubLayer
        fields = (
            "name",
            "layer",
            "created_at",
            "updated_at",
            "reference",
        )
