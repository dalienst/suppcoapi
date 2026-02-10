# accounts/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from cart.models import Cart

User = get_user_model()


@receiver(post_save, sender=User)
def create_user_cart(sender, instance, created, **kwargs):
    """
    Automatically create a Cart when a new User is created.
    Works for regular users, vendors, customers, AND superusers.
    """
    if created:
        # You can make this conditional if you want carts only for certain roles
        # if instance.is_customer or instance.is_superuser:
        Cart.objects.create(customer=instance)
