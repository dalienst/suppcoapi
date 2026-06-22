from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
from django.contrib.auth import get_user_model

from layers.models import Layer
from inventory.models import Inventory
from sublayers.serializers import SubLayerSerializer
from products.serializers import MiniProductSerializer

User = get_user_model()


class LayerSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    name = serializers.CharField(
        max_length=255,
    )
    inventory = serializers.SlugRelatedField(
        slug_field="inventory_code", queryset=Inventory.objects.all()
    )
    sublayers = SubLayerSerializer(many=True, read_only=True)
    products = MiniProductSerializer(source="layer_products", many=True, read_only=True)
    inventory_details = serializers.SerializerMethodField()
    user_details = serializers.SerializerMethodField()

    class Meta:
        model = Layer
        fields = (
            "id",
            "user",
            "name",
            "inventory",
            "created_at",
            "updated_at",
            "reference",
            "user_details",
            "inventory_details",
            "sublayers",
            "products",
        )
        validators = [
            UniqueTogetherValidator(
                queryset=Layer.objects.all(),
                fields=["inventory", "name"],
                message="Layer with this name already exists in this inventory.",
            )
        ]

    def get_inventory_details(self, obj):
        return {
            "inventory_code": obj.inventory.inventory_code,
            "name": obj.inventory.name,
            "company": {
                "name": obj.inventory.company.name,
            },
        }

    def get_user_details(self, obj):
        return {
            "username": obj.user.username,
            "email": obj.user.email,
            "reference": obj.user.reference,
            "account_type": obj.user.account_type,
        }
