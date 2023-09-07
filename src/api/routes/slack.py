"""Slack Commands Router."""

from datetime import date

from fastapi import APIRouter, Depends, Request
from src.db.repositories.leetcode_updates import LeetcodeUpdateRepository
from src.services.slack import send_message_to_channel
from src.api.dependencies.database import get_repository
from src.db.repositories.users import UserRepository
from src.models.users import CreateUserClient
from src.models.slack_payload import SlackPayload

from src.utils.parse_slack_payload import parse_slack_payload
from src.utils.validators import is_valid_number
from src.utils.split_string import split_name
from src.utils.strings import (
    ACCOUNT_CREATED,
    ALREADY_HAVE_AN_ACCOUNT,
    ALREADY_SENT_UPDATE,
    DONT_HAVE_AN_ACCOUNT,
    HELLO,
    INVALID_NUMBER,
    NO_UPDATE,
)
from src.utils.daytime_to_weekday import format_date


router = APIRouter()


@router.post("/hello")
async def hello(
    payload: Request,
) -> None:
    """Welcome Message."""
    slack_response: SlackPayload = parse_slack_payload(str(await payload.body())[1:])
    send_message_to_channel(slack_response.channel_id, slack_response.user_id, HELLO)


@router.post("/update", status_code=200)
async def update(
    payload: Request,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    leetcode_update_repo: LeetcodeUpdateRepository = Depends(
        get_repository(LeetcodeUpdateRepository)
    ),
) -> None:
    """Retrieve user's update."""
    slack_response: SlackPayload = parse_slack_payload(str(await payload.body())[1:])
    # validate if user has created an account.
    if not await user_repo.get_user_by_slack_id(slack_response.user_id):
        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, DONT_HAVE_AN_ACCOUNT
        )
        return
    if not is_valid_number(slack_response.text):
        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, INVALID_NUMBER
        )
        return

    # Add to database
    leetcode_record = await leetcode_update_repo.add_new_leetcode_update(
        new_leetcode_update=slack_response.text,
        slack_id=slack_response.user_id,
        date=date.today(),
    )
    if leetcode_record:
        # Send confirmation message
        message = f"Thanks for the update. Your leetcode update has been stored successfully. You solved {slack_response.text} questions today. Good work!.\n\nWe go again tomorrow."
        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, message
        )
        return
    send_message_to_channel(
        slack_response.channel_id, slack_response.user_id, ALREADY_SENT_UPDATE
    )


@router.post("/create")
async def create(
    payload: Request,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
) -> None:
    """Create a new user."""
    # Parse payload into model.
    slack_response: SlackPayload = parse_slack_payload(str(await payload.body())[1:])

    # Check if user already exists
    if not await user_repo.get_user_by_slack_id(slack_id=slack_response.user_id):
        fname, lname = split_name(slack_response.text)
        user = CreateUserClient(
            first_name=fname, last_name=lname, slack_id=slack_response.user_id
        )

        user = await user_repo.add_new_user(new_user=user)
        if user:
            # Send confirmation message
            send_message_to_channel(
                slack_response.channel_id,
                slack_response.user_id,
                ACCOUNT_CREATED,
            )
            return

        # Account already created.
        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, ALREADY_HAVE_AN_ACCOUNT
        )


@router.post("/weekly-report")
async def weekly_report(
    payload: Request,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    leetcode_update_repo: LeetcodeUpdateRepository = Depends(
        get_repository(LeetcodeUpdateRepository)
    ),
) -> None:
    """Send weekly report of leetcode update."""
    slack_response: SlackPayload = parse_slack_payload(str(await payload.body())[1:])
    # validate if user has created an account.
    if not await user_repo.get_user_by_slack_id(slack_response.user_id):
        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, DONT_HAVE_AN_ACCOUNT
        )
        return

    # Get user's leetcode updates
    leetcode_updates = await leetcode_update_repo.get_users_leetcode_update_weekly(
        slack_id=slack_response.user_id, date=date.today()
    )

    # Send message
    if leetcode_updates:
        count = sum(
            leetcode_update.leetcode_update for leetcode_update in leetcode_updates
        )
        messages = [
            f"On {format_date(leetcode_update.date)}, you solved {leetcode_update.leetcode_update} questions."
            for leetcode_update in leetcode_updates
        ]

        message = "\n".join(messages)
        summary_message = f"For this week, you've solved a total of {count} Leetcode questions. Congratulations!"
        combined_message = f"{message}\n\n{summary_message}"

        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, combined_message
        )
        return
    send_message_to_channel(
        slack_response.channel_id, slack_response.user_id, NO_UPDATE
    )


@router.post("/history")
async def history(
    payload: Request,
    user_repo: UserRepository = Depends(get_repository(UserRepository)),
    leetcode_update_repo: LeetcodeUpdateRepository = Depends(
        get_repository(LeetcodeUpdateRepository)
    ),
) -> None:
    """Send users entire leetcode update history."""
    slack_response: SlackPayload = parse_slack_payload(str(await payload.body())[1:])
    # validate if user has created an account.
    if not await user_repo.get_user_by_slack_id(slack_response.user_id):
        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, DONT_HAVE_AN_ACCOUNT
        )
        return

    # Get user's leetcode updates
    leetcode_updates = await leetcode_update_repo.get_all_of_users_leetcode_update(
        slack_id=slack_response.user_id
    )
    # Send message
    if leetcode_updates:
        count = sum(
            leetcode_update.leetcode_update for leetcode_update in leetcode_updates
        )
        messages = [
            f"On {format_date(leetcode_update.date)}, you solved {leetcode_update.leetcode_update} questions."
            for leetcode_update in leetcode_updates
        ]

        message = "\n".join(messages)
        summary_message = (
            f"You've solved a total of {count} Leetcode questions. Nice work!"
        )
        combined_message = f"{message}\n\n{summary_message}"

        send_message_to_channel(
            slack_response.channel_id, slack_response.user_id, combined_message
        )
        return

    send_message_to_channel(
        slack_response.channel_id, slack_response.user_id, NO_UPDATE
    )


# @router.post("/create-reminder")
# async def create_reminder(payload: Request, background_tasks: BackgroundTasks) -> None:
#     """Initiate scheduler to send daily reminders."""
#     slack_response: SlackPayload = parse_slack_payload(str(await payload.body())[1:])
#     background_tasks.add_task(start_reminder, slack_response.channel_id)
#     send_message_to_channel(
#         slack_response.channel_id, slack_response.user_id, REMINDER_CREATED
#     )
#     return JSONResponse({"status": "success"})
