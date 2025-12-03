from django.contrib import admin

from electricity.models import Electricity


class ElectricityAdmin(admin.ModelAdmin):
    list_display = (
        "reference",
        "created_at",
        "updated_at",
        "product_name",
        "specifications",
        "bracket",
        "branch",
        "company",
        "layer",
        "site",
        "sublayer",
        "sublayeritem",
        "user",
    )
    list_filter = (
        "reference",
        "created_at",
        "updated_at",
        "product_name",
        "specifications",
        "bracket",
        "branch",
        "company",
        "layer",
        "site",
        "sublayer",
        "sublayeritem",
        "user",
    )
    search_fields = (
        "reference",
        "created_at",
        "updated_at",
        "product_name",
        "specifications",
        "bracket",
        "branch",
        "company",
        "layer",
        "site",
        "sublayer",
        "sublayeritem",
        "user",
    )


admin.site.register(Electricity, ElectricityAdmin)
