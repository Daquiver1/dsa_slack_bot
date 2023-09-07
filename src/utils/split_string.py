"""Split name."""


from typing import Tuple


def split_name(text: str) -> Tuple[str, str]:
    """Split text into first name and last name."""
    # Split the full name into words
    name_parts = text.split()

    # Assuming the last word is the last name
    first_name = " ".join(name_parts[:-1])
    last_name = name_parts[-1]
    return first_name, last_name
