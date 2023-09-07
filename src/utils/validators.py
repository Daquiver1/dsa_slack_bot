"""Validators for the application."""


def is_valid_number(input_str: str) -> bool:
    """Validate if the input is a number and is between the ranges of 0 and 50."""
    if input_str.isnumeric() and int(input_str) > 0 and int(input_str) < 49:
        return True
    return False
