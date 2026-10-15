"""Validator for international phone numbers."""

from django.core.validators import RegexValidator

PHONE_NUMBER_PATTERN = r"^\+?[1-9]\d{7,14}$"

validate_phone_number = RegexValidator(
    regex=PHONE_NUMBER_PATTERN,
    message="Enter a valid phone number with country code, for example +923001234567.",
)
