"""Helper function to extract day of the week from a date string."""
from datetime import date


def format_date(date_str: date) -> str:
    """Helper function format date object to Thursday, 24 December 2020 format."""
    try:
        return date_str.strftime("%A %d %B %Y")
    except ValueError:
        return "Invalid Date Format"
