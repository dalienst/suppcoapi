from django.contrib import admin

from paymentoptions.models import PaymentOption


class PaymentOptionAdmin(admin.ModelAdmin):
    list_display = ["name", "payment_type", "min_deposit_percentage", "is_active"]
    list_filter = ["payment_type", "is_active"]
    search_fields = ["name", "description"]
    ordering = ["-created_at"]


admin.site.register(PaymentOption, PaymentOptionAdmin)
