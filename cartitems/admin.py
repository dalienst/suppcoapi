from django.contrib import admin

from cartitems.models import CartItem


@admin.register(CartItem)
class CartItemAdmin(admin.ModelAdmin):
    list_display = ("reference", "cart", "product", "quantity")
    list_filter = ("cart", "product")
    search_fields = ("reference", "cart__user__username", "product__product_name")
