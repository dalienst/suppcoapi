from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from permissions.models import Permission


class PermissionSerializer(serializers.ModelSerializer):
    name = serializers.CharField(
        validators=[UniqueValidator(queryset=Permission.objects.all())]
    )
    codename = serializers.CharField(
        validators=[UniqueValidator(queryset=Permission.objects.all())]
    )

    class Meta:
        model = Permission
        fields = (
            "name",
            "codename",
            "description",
            "reference",
            "created_at",
            "updated_at",
        )
