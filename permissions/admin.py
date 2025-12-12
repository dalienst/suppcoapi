from django.contrib import admin

from permissions.models import Permission


class PermissionAdmin(admin.ModelAdmin):
    list_display = ("name", "codename")
    search_fields = ("name", "codename")
    list_filter = ("name", "codename")
    ordering = ("name", "codename")


admin.site.register(Permission, PermissionAdmin)
