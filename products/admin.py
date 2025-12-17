from django.contrib import admin

from products.models import Product


class ProductAdmin(admin.ModelAdmin):
    list_display = (
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
        "reference",
        "created_at",
        "updated_at",
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
        "source_location",
        "product_name",
        "specifications",
        "reference",
        "created_at",
        "updated_at",
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
        "source_location",
        "product_name",
        "specifications",
        "reference",
        "created_at",
        "updated_at",
    )


admin.site.register(Product, ProductAdmin)
