from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from brackets.models import Bracket
from sublayeritems.models import SublayerItem
from django.contrib.auth import get_user_model

User = get_user_model()


class BracketSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    sublayeritem = serializers.SlugRelatedField(
        slug_field="reference", queryset=SublayerItem.objects.all()
    )
    name = serializers.CharField()
    sublayeritem_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Bracket
        fields = (
            "user",
            "name",
            "sublayeritem",
            "created_at",
            "updated_at",
            "reference",
            "user_details",
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

    def get_user_details(self, obj):
        return {
            "username": obj.user.username,
            "email": obj.user.email,
            "reference": obj.user.reference,
            "account_type": obj.user.account_type,
        }
