import os
import schedule
import time
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

from strings import MORNING_TEXT, EVENING_TEXT

logging.basicConfig(level=logging.DEBUG)
CHANNEL_ID = "C05N52FH0SF"


def sendMessage(slack_client, txt):
    # make the POST request through the python slack client

    # check if the request was a success
    try:
        response = slack_client.conversations_members(channel=CHANNEL_ID)
        if response["ok"]:
            user_ids = response["members"]
            user_ids.remove("U05QD5SS81W")
        else:
            print(f"Error getting user list: {response['error']}")
        for user_id in user_ids:
            slack_client.chat_postMessage(
                channel="#testbot",
                text=f"Hello <@{user_id}>, hope you are good. {txt}.",
            )

    except SlackApiError as e:
        logging.error("Request to Slack API Failed: {}.".format(e.response.status_code))
        logging.error(e.response)


if __name__ == "__main__":
    SLACK_BOT_TOKEN = "xoxb-3769684266272-5829196892064-rCWQ064aWXBZnjru5N1LEEsQ"  # os.environ["SLACK_BOT_TOKEN"]
    slack_client = WebClient(SLACK_BOT_TOKEN)
    logging.debug("authorized slack client")

    # # For testing
    # msg = "<@U043TGDDV7G|Baaba>, <@U04QE7S6AHY|Senpai>, <@U04R0GQGEBB|Nai>, please send in your update."
    # schedule.every(10).seconds.do(lambda: sendMessage(slack_client))
    sendMessage(slack_client, MORNING_TEXT)

    # schedule.every().monday.at("13:15").do(lambda: sendMessage(slack_client, msg))
    logging.info("entering loop")

    # while True:
    #     schedule.run_pending()
    #     time.sleep(5)  # sleep for 5 seconds between checks on the scheduler
