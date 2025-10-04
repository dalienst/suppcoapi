from rest_framework import serializers

from employment.models import Employment
from roles.models import Role
from companies.models import Company


class EmploymentSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.SlugRelatedField(
        queryset=Company.objects.all(), slug_field="name"
    )
    role = serializers.SlugRelatedField(
        queryset=Role.objects.all(), slug_field="identity"
    )

    class Meta:
        model = Employment
        fields = (
            "user",
            "company",
            "role",
            "is_active",
            "identity",
            "created_at",
            "updated_at",
        )

    def validate(self, attrs):
        company = attrs.get("company")
        role = attrs.get("role")
        if role.company != company:
            raise serializers.ValidationError("Role is not in this company")
        return attrs
