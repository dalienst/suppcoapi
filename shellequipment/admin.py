from django.contrib import admin

from shellequipment.models import ShellEquipment


class ShellEquipmentAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
        "company",
        "branch",
        "site",
        "layer",
        "sublayer",
        "sublayeritem",
        "bracket",
    )
    search_fields = ("product_name", "specifications")
    ordering = ("-created_at",)


admin.site.register(ShellEquipment, ShellEquipmentAdmin)
