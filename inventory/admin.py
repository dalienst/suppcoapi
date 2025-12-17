from django.contrib import admin

from inventory.models import Inventory


class InventoryAdmin(admin.ModelAdmin):
    list_display = ("company", "user", "name", "inventory_code", "description")
    search_fields = ("company__name", "name", "inventory_code", "description")


admin.site.register(Inventory, InventoryAdmin)
