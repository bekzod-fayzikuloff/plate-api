from rest_framework.exceptions import ValidationError

from plate.resources import DEFAULT_PLATE_QUANTITY


def validate_amount_qs(amount: int | str) -> int:
    """Validate a amount query parameter"""
    if isinstance(amount, int):
        return amount or DEFAULT_PLATE_QUANTITY
    if amount.isdigit():
        validated_amount = int(amount)
        return validated_amount or DEFAULT_PLATE_QUANTITY
    if not amount:
        return DEFAULT_PLATE_QUANTITY
    raise ValidationError("Invalid amount value value should be a int or None")
