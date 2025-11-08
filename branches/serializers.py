from rest_framework import serializers

from branches.models import Branch
from companies.models import Company


class BranchSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.CharField(source="user.company.name", read_only=True)

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

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            company = user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("You are not a company owner")

        return Branch.objects.create(user=user, company=company, **validated_data)
