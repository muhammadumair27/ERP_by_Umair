"""Custom user model for the Manufacturing ERP.

The project identifies users by email address rather than by username, so this
model is defined before the first database migration is ever applied.
"""

from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.managers.user_manager import UserManager
from common.models.time_stamped_model import TimeStampedModel


class User(AbstractBaseUser, PermissionsMixin, TimeStampedModel):
    """Application user, uniquely identified by email address."""

    email = models.EmailField(_("email address"), unique=True)
    full_name = models.CharField(_("full name"), max_length=255)
    phone = models.CharField(_("phone number"), max_length=32, blank=True, default="")

    is_active = models.BooleanField(_("active"), default=True)
    is_staff = models.BooleanField(_("staff status"), default=False)
    must_change_password = models.BooleanField(_("must change password"), default=False)
    email_verified_at = models.DateTimeField(_("email verified at"), null=True, blank=True)

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    class Meta:
        verbose_name = _("user")
        verbose_name_plural = _("users")
        ordering = ("email",)
        indexes = [
            models.Index(fields=["is_active"], name="user_is_active_idx"),
            models.Index(fields=["is_staff"], name="user_is_staff_idx"),
        ]

    def __str__(self) -> str:
        return self.email

    def get_full_name(self) -> str:
        """Return the user's full name, falling back to the email address."""

        return self.full_name or self.email

    def get_short_name(self) -> str:
        """Return the first token of the user's name."""

        return (self.full_name or self.email).split(" ")[0]

    @property
    def is_verified(self) -> bool:
        """Whether the user's email address has been verified."""

        return self.email_verified_at is not None
