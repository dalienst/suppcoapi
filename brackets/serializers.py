from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from brackets.models import Bracket
from sublayeritems.models import SublayerItem


class BracketSerializer(serializers.ModelSerializer):
    sublayeritem = serializers.SlugRelatedField(
        slug_field="name", queryset=SublayerItem.objects.all()
    )
    name = serializers.CharField()

    class Meta:
        model = Bracket
        fields = (
            "name",
            "sublayeritem",
            "created_at",
            "updated_at",
            "reference",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Bracket.objects.all(),
                fields=["name", "sublayeritem"],
                message="Bracket with this name already exists in this sublayeritem.",
            )
        ]
