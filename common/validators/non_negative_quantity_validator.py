"""Validator for non-negative quantities and amounts."""

from decimal import Decimal

from django.core.validators import MinValueValidator

validate_non_negative_quantity = MinValueValidator(
    limit_value=Decimal("0"),
    message="Quantity must be greater than or equal to 0.",
)
