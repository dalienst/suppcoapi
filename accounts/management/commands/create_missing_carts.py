from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from cart.models import Cart


class Command(BaseCommand):
    help = "Creates a cart for users who do not have one"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        users = User.objects.all()
        created_count = 0
        existing_count = 0

        self.stdout.write("Checking for missing carts...")

        for user in users:
            cart, created = Cart.objects.get_or_create(user=user)
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created cart for user: {user.username}")
                )
            else:
                existing_count += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"Finished processing. Created {created_count} carts. {existing_count} users already had a cart."
            )
        )
