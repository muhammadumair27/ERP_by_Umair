"""Application configuration for the accounts app."""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Configure the accounts application."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.accounts"
    label = "accounts"
    verbose_name = "Accounts"
