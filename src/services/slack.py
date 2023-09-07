"""Slack service to send messages to a channel."""
from typing import List
import schedule
import time
import logging
from slack_sdk import WebClient

from src.utils.strings import REMINDER_TEXT

from src.core.config import SLACK_BOT_TOKEN, BOT_ID

slack_client = WebClient(SLACK_BOT_TOKEN)


def send_message_to_channel(channel_id: str, slack_id: str, message: str) -> WebClient:
    """Send message to a specified channel."""
    return slack_client.chat_postMessage(
        channel=channel_id, text=f"Hello <@{slack_id}>,\n\n{message}"
    )


def send_reminder_message_to_channel(channel_id: str) -> WebClient:
    """Get all the users in a channel and send a reminder to them."""
    print("About to send in message.")
    for slack_id in get_user_id_of_users_in_channel(channel_id=channel_id):
        send_message_to_channel(channel_id, slack_id, REMINDER_TEXT)


def get_user_id_of_users_in_channel(channel_id: str) -> List[str]:
    """Get all the users in a channel."""
    response = slack_client.conversations_members(channel=channel_id)
    if response["ok"]:
        user_ids = response["members"]
        user_ids.remove(BOT_ID)
        return user_ids
    return []


def start_reminder(channel_id: str) -> None:
    """Run the reminder background task."""
    schedule.every(10).seconds.do(lambda: send_reminder_message_to_channel(channel_id))
    logging.info("entering loop")

    while True:
        schedule.run_pending()
        time.sleep(13)  # sleep for 13 hours between checks on the scheduler
