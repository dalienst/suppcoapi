from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from brackets.models import Bracket
from sublayeritems.models import SublayerItem


class BracketSerializer(serializers.ModelSerializer):
    sublayeritem = serializers.SlugRelatedField(
        slug_field="reference", queryset=SublayerItem.objects.all()
    )
    name = serializers.CharField()
    sublayeritem_details = serializers.SerializerMethodField()

    class Meta:
        model = Bracket
        fields = (
            "name",
            "sublayeritem",
            "created_at",
            "updated_at",
            "reference",
            "sublayeritem_details",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Bracket.objects.all(),
                fields=["name", "sublayeritem"],
                message="Bracket with this name already exists in this sublayeritem.",
            )
        ]

    def get_sublayeritem_details(self, obj):
        return {
            "name": obj.sublayeritem.name,
        }
