from rest_framework import serializers

from sites.models import Site
from companies.models import Company


class SiteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.CharField(source="user.company.name", read_only=True)

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

    def create(self, validated_data):
        user = self.context["request"].user

        try:
            company = user.company
        except Company.DoesNotExist:
            raise serializers.ValidationError("You are not a company owner")
        
        return Site.objects.create(user=user, company=company, **validated_data)
