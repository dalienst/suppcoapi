from django.contrib import admin

from companies.models import Company

class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "email",
        "phone",
        "created_at",
    )
    ordering = ("-created_at",)
    list_filter = ("created_at", "user")
    search_fields = ("name", "email", "phone")


admin.site.register(Company, CompanyAdmin)
