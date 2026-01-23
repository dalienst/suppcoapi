from django.contrib import admin

from paymentplans.models import PaymentPlan


class PaymentPlanAdmin(admin.ModelAdmin):
    list_display = (
        "product",
        "user",
        "payment_option",
        "amount",
        "plan",
    )


admin.site.register(PaymentPlan, PaymentPlanAdmin)
