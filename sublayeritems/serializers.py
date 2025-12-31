from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from sublayeritems.models import SublayerItem
from sublayers.models import SubLayer
from brackets.serializers import BracketSerializer


class SublayerItemSerializer(serializers.ModelSerializer):
    sublayer = serializers.SlugRelatedField(
        slug_field="reference", queryset=SubLayer.objects.all()
    )
    name = serializers.CharField(
    )
    brackets = BracketSerializer(many=True, read_only=True)

    class Meta:
        model = SublayerItem
        fields = (
            "name",
            "sublayer",
            "created_at",
            "updated_at",
            "reference",
            "brackets",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=SublayerItem.objects.all(),
                fields=["name", "sublayer"],
                message="Sublayer Item with this name already exists in this sublayer.",
            )
        ]
