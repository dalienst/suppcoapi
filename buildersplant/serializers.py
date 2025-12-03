from rest_framework import serializers

from buildersplant.models import BuilderPlant
from companies.models import Company
from branches.models import Branch
from sites.models import Site


class BuilderPlantSerializer(serializers.ModelSerializer):
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
    image = serializers.ImageField(use_url=True, required=False)

    class Meta:
        model = BuilderPlant
        fields = (
            "user",
            "company",
            "branch",
            "site",
            "source_location",
            "product_name",
            "specifications",
            "image",
            "reference",
            "created_at",
            "updated_at",
        )
