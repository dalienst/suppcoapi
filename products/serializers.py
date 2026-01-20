from rest_framework import serializers

from companies.models import Company
from branches.models import Branch
from sites.models import Site
from layers.models import Layer
from sublayers.models import SubLayer
from sublayeritems.models import SublayerItem
from brackets.models import Bracket
from products.models import Product


class ProductSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.CharField(source="user.company.name", read_only=True)
    branch = serializers.SlugRelatedField(
        slug_field="identity", queryset=Branch.objects.all(), required=False
    )
    site = serializers.SlugRelatedField(
        slug_field="identity", queryset=Site.objects.all(), required=False
    )
    layer = serializers.SlugRelatedField(
        slug_field="reference", queryset=Layer.objects.all(), required=False
    )
    sublayer = serializers.SlugRelatedField(
        slug_field="reference", queryset=SubLayer.objects.all(), required=False
    )
    sublayeritem = serializers.SlugRelatedField(
        slug_field="reference", queryset=SublayerItem.objects.all(), required=False
    )
    bracket = serializers.SlugRelatedField(
        slug_field="reference", queryset=Bracket.objects.all(), required=False
    )
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = Product
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
            "sku",
            "reference",
            "created_at",
            "updated_at",
        )

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            company = user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("You are not a company owner")

        return Product.objects.create(company=company, **validated_data)
