"""Setting up configs."""

# Third party imports
import logging

from starlette.config import Config

config = Config(".env")

log = logging.getLogger(__name__)


PROJECT_NAME = "slack-leetcode-update-api"
VERSION = "1.0"
API_PREFIX = "/api"

SLACK_BOT_TOKEN = config("SLACK_BOT_TOKEN", cast=str)
BOT_ID = config("BOT_ID", cast=str)
