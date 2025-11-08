from rest_framework import serializers

from branches.models import Branch
from companies.models import Company


class BranchSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )

    class Meta:
        model = Branch
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
