from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from sublayeritems.models import SublayerItem
from sublayers.models import SubLayer


class SublayerItemSerializer(serializers.ModelSerializer):
    sublayer = serializers.SlugRelatedField(
        slug_field="name", queryset=SubLayer.objects.all()
    )
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=SublayerItem.objects.all())]
    )

    class Meta:
        model = SublayerItem
        fields = (
            "name",
            "sublayer",
            "created_at",
            "updated_at",
            "reference",
        )
