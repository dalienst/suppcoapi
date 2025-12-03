from rest_framework import serializers

from shellequipment.models import ShellEquipment
from companies.models import Company
from branches.models import Branch
from sites.models import Site
from layers.models import Layer
from sublayers.models import SubLayer
from sublayeritems.models import SublayerItem
from brackets.models import Bracket


class ShellEquipmentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.SlugRelatedField(
        slug_field="identity", queryset=Company.objects.all()
    )
    branch = serializers.SlugRelatedField(
        slug_field="identity", queryset=Branch.objects.all(), required=False
    )
    site = serializers.SlugRelatedField(
        slug_field="identity", queryset=Site.objects.all(), required=False
    )
    layer = serializers.SlugRelatedField(
        slug_field="name", queryset=Layer.objects.all(), required=False
    )
    sublayer = serializers.SlugRelatedField(
        slug_field="name", queryset=SubLayer.objects.all(), required=False
    )
    sublayeritem = serializers.SlugRelatedField(
        slug_field="name", queryset=SublayerItem.objects.all(), required=False
    )
    bracket = serializers.SlugRelatedField(
        slug_field="name", queryset=Bracket.objects.all(), required=False
    )
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = ShellEquipment
        fields = (
            "user",
            "company",
            "branch",
            "site",
            "layer",
            "sublayer",
            "sublayeritem",
            "bracket",
            "source_location",
            "product_name",
            "specifications",
            "image",
            "reference",
            "created_at",
            "updated_at",
        )
