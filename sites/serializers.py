from rest_framework import serializers

from sites.models import Site
from companies.models import Company


class SiteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )

    class Meta:
        model = Site
        fields = (
            "user",
            "name",
            "company",
            "address",
            "reference",
            "identity",
            "created_at",
            "updated_at",
        )
