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

    def validate(self, attrs):
        # Only create roles for your company
        company = attrs.get("company")
        name = attrs.get("name")
        if company.user != self.context["request"].user:
            raise serializers.ValidationError(
                "You can only create roles for your company"
            )

        # prevent creating roles with the same name despite the case
        if Role.objects.filter(name__iexact=name, company=company).exists():
            raise serializers.ValidationError("Role with this name already exists")
        return super().validate(attrs)
