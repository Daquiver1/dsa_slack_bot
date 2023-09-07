"""Helper function."""
from urllib.parse import parse_qs

from src.models.slack_payload import SlackPayload


# The given text
def parse_slack_payload(token: str) -> SlackPayload:
    """Helper function to parse the payload received from slack to slack payload class."""
    # Parse the text into a dictionary
    data = parse_qs(token)  # Splits into key and value. Value is in a list.
    parsed_data_single = {
        key: values[0] for key, values in data.items()
    }  # Extract the first value of the list
    return SlackPayload(**parsed_data_single)
