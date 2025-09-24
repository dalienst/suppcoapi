from rest_framework import serializers

from roles.models import Role
from companies.models import Company


class RoleSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    name = serializers.CharField(max_length=2555, required=True)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )
    is_head = serializers.BooleanField(default=False)

    class Meta:
        model = Role
        fields = (
            "user",
            "name",
            "is_head",
            "company",
            "identity",
            "created_at",
            "updated_at",
        )
