"""Model for the payload sent by slack."""

from pydantic import BaseModel


class SlackPayload(BaseModel):
    """Slack payload."""

    team_id: str
    channel_id: str
    user_id: str
    command: str
    text: str = ""
    response_url: str
    trigger_id: str
    api_app_id: str

    class Config:
        """Config class."""

        # This tells Pydantic to allow extra fields not defined in the model
        extra = "allow"
