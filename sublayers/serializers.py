from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from sublayers.models import SubLayer
from layers.models import Layer
from sublayeritems.serializers import SublayerItemSerializer
from products.serializers import MiniProductSerializer

User = get_user_model()


class SubLayerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    layer = serializers.SlugRelatedField(
        queryset=Layer.objects.all(), slug_field="reference"
    )
    name = serializers.CharField()
    sublayeritems = SublayerItemSerializer(many=True, read_only=True)
    products = MiniProductSerializer(source="sublayer_products", many=True, read_only=True)
    layer_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = SubLayer
        fields = (
            "id",
            "user",
            "name",
            "layer",
            "created_at",
            "updated_at",
            "reference",
            "user_details",
            "layer_details",
            "sublayeritems",
            "products",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=SubLayer.objects.all(),
                fields=["layer", "name"],
                message="SubLayer with this name already exists in this layer.",
            )
        ]

    def get_layer_details(self, obj):
        return {
            "name": obj.layer.name,
        }

    def get_user_details(self, obj):
        return {
            "username": obj.user.username,
            "email": obj.user.email,
        }
