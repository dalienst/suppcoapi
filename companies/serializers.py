from django.contrib.auth import get_user_model
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from companies.models import Company

User = get_user_model()


class CompanySerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        max_length=2550,
        validators=[UniqueValidator(queryset=Company.objects.all())],
        required=False,
    )
    user = serializers.CharField(read_only=True, source="user.email")
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=Company.objects.all())],
        required=False,
    )
    phone = serializers.CharField(
        max_length=15,
        validators=[UniqueValidator(queryset=Company.objects.all())],
        required=False,
    )
    logo = serializers.ImageField(use_url=True, required=False)
    registration_number = serializers.CharField(
        validators=[UniqueValidator(queryset=Company.objects.all())], required=False
    )
    kra_pin = serializers.CharField(
        validators=[UniqueValidator(queryset=Company.objects.all())], required=False
    )
    vat_number = serializers.CharField(
        validators=[UniqueValidator(queryset=Company.objects.all())], required=False
    )

    class Meta:
        model = Company
        fields = (
            "id",
            "user",
            "name",
            "email",
            "phone",
            "logo",
            "address",
            "registration_number",
            "kra_pin",
            "currency",
            "fiscal_year",
            "vat_number",
            "vat_compliance",
            "type",
            "identity",
            "created_at",
            "updated_at",
            "reference",
        )
        
