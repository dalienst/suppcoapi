from django.contrib import admin

from buildersplant.models import BuilderPlant


class BuilderPlantAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "company",
        "branch",
        "site",
        "source_location",
        "product_name",
        "specifications",
        "image",
        "reference",
        "created_at",
        "updated_at",
    )
    list_filter = (
        "user",
        "company",
        "branch",
        "site",
        "source_location",
        "product_name",
        "specifications",
        "image",
        "reference",
        "created_at",
        "updated_at",
    )
    search_fields = (
        "user",
        "company",
        "branch",
        "site",
        "source_location",
        "product_name",
        "specifications",
        "image",
        "reference",
        "created_at",
        "updated_at",
    )


admin.site.register(BuilderPlant, BuilderPlantAdmin)
