"""DB Repository for leetcode update table."""

import logging
from typing import List, Optional
from datetime import date

from databases import Database

from src.models.leetcode_updates import LeetcodeUpdatePublic
from src.db.repositories.base import BaseRepository

logger = logging.getLogger(__name__)

ADD_LEETCODE_UPDATE_QUERY = """
INSERT INTO leetcode_updates (leetcode_update, date, posters_slack_id)
    VALUES (:leetcode_update, :date, :posters_slack_id);
"""

GET_LEETCODE_UPDATE_BY_USERNAME_QUERY = """
    SELECT *
    FROM leetcode_updates
    WHERE posters_slack_id = :posters_slack_id;
    """

GET_ALL_WEEKLY_LEETCODE_UPDATE_BY_USERNAME_QUERY = """
    SELECT *
    FROM leetcode_updates
    WHERE posters_slack_id = :posters_slack_id
    AND date >= date('now', '-7 days')
    """

GET_ALL_LEETCODE_UPDATE_BY_USERNAME_QUERY = """
    SELECT *
    FROM leetcode_updates
    WHERE posters_slack_id = :posters_slack_id
    AND date >= date('now', '-28 days')
    """

DELETE_LEETCODE_UPDATE_BY_USERNAME_QUERY = """
    DELETE FROM leetcode_updates
    WHERE posters_slack_id = :posters_slack_id;
    """


class LeetcodeUpdateRepository(BaseRepository):
    """All db actions associated with the leetcode_update resource."""

    def __init__(self, db: Database) -> None:
        """Initialize db."""
        super().__init__(db)

    async def add_new_leetcode_update(
        self, *, new_leetcode_update: int, slack_id: str, date: date
    ) -> Optional[int]:
        """Create new leetcode updates data."""
        if await self.get_users_leetcode_update_by_date(slack_id):
            return None

        await self.db.fetch_one(
            query=ADD_LEETCODE_UPDATE_QUERY,
            values={
                "leetcode_update": new_leetcode_update,
                "posters_slack_id": slack_id,
                "date": date,
            },
        )
        return new_leetcode_update

    async def get_all_of_users_leetcode_update(
        self, slack_id: str
    ) -> Optional[List[LeetcodeUpdatePublic]]:
        """Get all of users leetcode update data."""
        leetcode_update_record = await self.db.fetch_all(
            query=GET_ALL_LEETCODE_UPDATE_BY_USERNAME_QUERY,
            values={"posters_slack_id": slack_id},
        )
        if leetcode_update_record:
            return [
                LeetcodeUpdatePublic(**leetcode_update)
                for leetcode_update in leetcode_update_record
            ]
        return None

    async def get_users_leetcode_update_weekly(
        self, slack_id: str, date: date
    ) -> Optional[List[LeetcodeUpdatePublic]]:
        """Get users weekly leetcode update."""
        leetcode_update_record = await self.db.fetch_all(
            query=GET_ALL_WEEKLY_LEETCODE_UPDATE_BY_USERNAME_QUERY,
            values={"posters_slack_id": slack_id},
        )
        if leetcode_update_record:
            return [
                LeetcodeUpdatePublic(**leetcode_update)
                for leetcode_update in leetcode_update_record
            ]
        return None

    async def get_users_leetcode_update_by_date(
        self, slack_id: str
    ) -> Optional[LeetcodeUpdatePublic]:
        """Get current day users leetcode update data."""
        leetcode_update_record = await self.db.fetch_one(
            query=GET_LEETCODE_UPDATE_BY_USERNAME_QUERY,
            values={"posters_slack_id": slack_id},
        )
        if leetcode_update_record:
            return LeetcodeUpdatePublic(**leetcode_update_record)
        return None
