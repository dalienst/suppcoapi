from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
)
from django.db import models

from accounts.abstracts import (
    AbstractProfileModel,
    TimeStampedModel,
    UniversalIdModel,
    ReferenceModel,
)
from accounts.utils import generate_username


class UserManager(BaseUserManager):
    use_in_migrations: bool = True

    def _create_user(self, email, password, **kwargs):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **kwargs)
        user.set_password(password)
        user.save()
        return user

    def create_user(self, email, password=None, **kwargs):
        kwargs.setdefault("is_staff", False)
        kwargs.setdefault("is_superuser", False)
        return self._create_user(email, password, **kwargs)

    def create_superuser(self, email, password, **kwargs):
        kwargs.setdefault("is_staff", True)
        kwargs.setdefault("is_superuser", True)
        kwargs.setdefault("is_active", True)

        if kwargs.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if kwargs.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")
        if kwargs.get("is_active") is not True:
            raise ValueError("Superuser must have is_active=True.")

        return self._create_user(email, password, **kwargs)


class User(
    AbstractBaseUser,
    PermissionsMixin,
    UniversalIdModel,
    TimeStampedModel,
    AbstractProfileModel,
    ReferenceModel,
):
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(
        max_length=255, unique=True, default=generate_username, editable=False
    )
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_contractor = models.BooleanField(default=False)
    is_supplier = models.BooleanField(default=False)
    account_type = models.CharField(max_length=20, default="user", editable=False)

    # assignments
    assigned_site = models.ForeignKey(
        "sites.Site",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_staff",
    )
    assigned_branch = models.ForeignKey(
        "branches.Branch",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="assigned_staff",
    )

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]

    objects = UserManager()

    def __str__(self):
        return self.email
