"""Validator for business tax and registration numbers."""

from django.core.validators import RegexValidator

TAX_NUMBER_PATTERN = r"^[A-Za-z0-9\-]{5,32}$"

validate_tax_number = RegexValidator(
    regex=TAX_NUMBER_PATTERN,
    message="Enter a valid tax number of 5 to 32 letters, digits or hyphens.",
)
