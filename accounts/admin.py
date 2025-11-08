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
                    "is_contractor",
                    "is_supplier",
                    "assigned_site",
                    "assigned_branch",
                )
            },
        ),
        (_("Account"), {"fields": ("account_type",)}),  # Optional: separate section
    )
    add_fieldsets = ((None, {"classes": ("wide",), "fields": ("email", "password")}),)
    list_display = (
        "email",
        "first_name",
        "last_name",
        "is_staff",
        "is_active",
        "is_contractor",
        "is_supplier",
        "account_type",
    )
    search_fields = ("email", "first_name", "last_name")
    ordering = ("email",)
    list_filter = (
        "is_staff",
        "is_active",
        "is_contractor",
        "is_supplier",
        "assigned_site",
        "assigned_branch",
        "account_type",
    )

    readonly_fields = ("account_type", "username", "reference")


admin.site.register(User, UserAdmin)
