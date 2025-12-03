from django.contrib import admin

from plumbing.models import Plumbing


class PlumbingAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "user",
        "company",
        "branch",
        "site",
        "layer",
        "sublayer",
        "sublayeritem",
        "bracket",
        "source_location",
        "product_name",
        "specifications",
    )
    list_filter = (
        "user",
        "company",
        "branch",
        "site",
        "layer",
        "sublayer",
        "sublayeritem",
        "bracket",
    )
    search_fields = (
        "user",
        "company",
        "branch",
        "site",
        "layer",
        "sublayer",
        "sublayeritem",
        "bracket",
    )


admin.site.register(Plumbing, PlumbingAdmin)
