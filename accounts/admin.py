from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User = get_user_model()


class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            _("Personal info"),
            {
                "fields": (
                    "first_name",
                    "last_name",
                    "avatar",
                    "identification",
                    "kra_pin",
                    "phone",
                )
            },
        ),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (_("Important dates"), {"fields": ("last_login",)}),
        (
            _("Profile"),
            {
                "fields": (
                    "reference",
                    "slug",
                    "is_contractor",
                    "is_supplier",
                    "is_subcontractor",
                )
            },
        ),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("email", "password"),
            },
        ),
    )
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_contractor",
        "is_supplier",
        "is_subcontractor",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    list_filter = (
        "is_staff",
        "is_active",
        "is_contractor",
        "is_supplier",
        "is_subcontractor",
    )


admin.site.register(User, UserAdmin)
