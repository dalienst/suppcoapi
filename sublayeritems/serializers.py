from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from sublayeritems.models import SublayerItem
from sublayers.models import SubLayer
from brackets.serializers import BracketSerializer


class SublayerItemSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    sublayer = serializers.SlugRelatedField(
        slug_field="reference", queryset=SubLayer.objects.all()
    )
    name = serializers.CharField()
    brackets = BracketSerializer(many=True, read_only=True)
    sublayer_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = SublayerItem
        fields = (
            "user",
            "name",
            "sublayer",
            "created_at",
            "updated_at",
            "reference",
            "user_details",
            "sublayer_details",
            "brackets",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=SublayerItem.objects.all(),
                fields=["name", "sublayer"],
                message="Sublayer Item with this name already exists in this sublayer.",
            )
        ]

    def get_sublayer_details(self, obj):
        return {
            "name": obj.sublayer.name,
        }

    def get_user_details(self, obj):
        return {
            "username": obj.user.username,
            "email": obj.user.email,
            "reference": obj.user.reference,
            "account_type": obj.user.account_type,
        }
