from rest_framework import serializers
from django.contrib.auth import get_user_model

from sites.models import Site
from companies.models import Company

User = get_user_model()


class SiteSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source="user.username", read_only=True)
    company = serializers.CharField(source="user.company.name", read_only=True)
    head = serializers.CharField(source="head.username", read_only=True)

    class Meta:
        model = Site
        fields = (
            "user",
            "name",
            "company",
            "head",
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
