from rest_framework import serializers

from companies.models import Company
from branches.models import Branch
from sites.models import Site
from layers.models import Layer
from sublayers.models import SubLayer
from sublayeritems.models import SublayerItem
from brackets.models import Bracket
from products.models import Product
from paymentoptions.models import PaymentOption
from paymentoptions.serializers import PaymentOptionSerializer


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
    payment_options = serializers.SlugRelatedField(
        slug_field="reference",
        queryset=PaymentOption.objects.all(),
        required=False,
        many=True,
    )
    payment_options_details = serializers.SerializerMethodField()

    def get_payment_options_details(self, obj):
        return PaymentOptionSerializer(obj.payment_options.all(), many=True).data

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
            "quantity",
            "unit",
            "price",
            "reference",
            "created_at",
            "updated_at",
            "payment_options",
            "payment_options_details",
        )

    def create(self, validated_data):
        user = self.context["request"].user
        payment_options = validated_data.pop("payment_options", [])

        try:
            company = user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("You are not a company owner")

        product = Product.objects.create(company=company, **validated_data)
        product.payment_options.set(payment_options)
        return product

    def update(self, instance, validated_data):
        payment_options = validated_data.pop("payment_options", None)
        if payment_options is not None:
            instance.payment_options.set(payment_options)
        return super().update(instance, validated_data)
