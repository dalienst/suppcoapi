from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from brackets.models import Bracket
from sublayeritems.models import SublayerItem


class BracketSerializer(serializers.ModelSerializer):
    sublayeritem = serializers.SlugRelatedField(
        slug_field="name", queryset=SublayerItem.objects.all()
    )
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Bracket.objects.all())]
    )

    class Meta:
        model = Bracket
        fields = (
            "name",
            "sublayeritem",
            "created_at",
            "updated_at",
            "reference",
        )
