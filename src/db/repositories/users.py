"""DB Repository for users table."""

import logging
from typing import Union

from databases import Database

from src.db.repositories.base import BaseRepository
from src.models.users import CreateUserClient, UserInDB, UserPublic

logger = logging.getLogger(__name__)

ADD_USER_QUERY = """
    INSERT INTO users (first_name, last_name, slack_id)
    VALUES (:first_name, :last_name, :slack_id);
"""

GET_USER_BY_SLACK_ID_QUERY = """
    SELECT *
    FROM users
    WHERE slack_id = :slack_id;
    """

GET_USER_BY_ID_QUERY = """
    SELECT *
    FROM users
    WHERE id = :id;
    """

DELETE_USER_BY_SLACK_ID_QUERY = """
    DELETE FROM users
    WHERE slack_id = :slack_id;
    """

DELETE_USER_BY_ID_QUERY = """
    DELETE FROM users
    WHERE id = :id;
    """

UPDATE_USER_BY_SLACK_ID_QUERY = """
    UPDATE users
    SET first_name = :first_name,
        last_name = :last_name,
=    WHERE slack_id = :slack_id;
    """


class UserRepository(BaseRepository):
    """All db actions associated with the user resource."""

    def __init__(self, db: Database) -> None:
        """Initialize db."""
        super().__init__(db)

    async def add_new_user(self, *, new_user: CreateUserClient) -> UserInDB:
        """Create new users data."""
        if await self.get_user_by_slack_id(slack_id=new_user.slack_id):
            return None  # user exists

        await self.db.fetch_one(
            query=ADD_USER_QUERY,
            values=new_user.model_dump(),
        )
        created_user = await self.get_user_by_slack_id(slack_id=new_user.slack_id)
        return created_user

    async def get_user_by_slack_id(
        self, slack_id: str
    ) -> Union[UserInDB, UserPublic, None]:
        """Get user data."""
        user_record = await self.db.fetch_one(
            query=GET_USER_BY_SLACK_ID_QUERY,
            values={"slack_id": slack_id},
        )
        if user_record:
            print(user_record)
            user = UserInDB(**user_record)
            return user
        return None

    async def get_user_by_id(self, id: str) -> Union[UserInDB, UserPublic, None]:
        """Get user data."""
        user_record = await self.db.fetch_one(
            query=GET_USER_BY_ID_QUERY,
            values={"id": id},
        )
        if user_record:
            user = UserInDB(**user_record)
            return user
        return None

    async def update_user_by_slack_id(
        self, updated_user: UserPublic
    ) -> Union[UserInDB, UserPublic, None]:
        """Update user data."""
        if not await self.get_user_by_slack_id(slack_id=updated_user.slack_id):
            return None  # user doesn't exist

        await self.db.fetch_one(
            query=UPDATE_USER_BY_SLACK_ID_QUERY,
            values=updated_user,
        )
        return await self.get_user_by_slack_id(slack_id=updated_user.slack_id)

    async def delete_user_by_username(self, *, slack_id: str) -> str:
        """Delete user data by str."""
        if not await self.get_user_by_slack_id(slack_id=slack_id):
            return None  # user doesn't exist

        return await self.db.execute(
            query=DELETE_USER_BY_SLACK_ID_QUERY,
            values={"slack_id": slack_id},
        )

    async def delete_user_by_id(self, *, id: str) -> str:
        """Delete user data by id."""
        if not await self.get_user_by_id(id=id):
            return None  # user doesn't exist

        return await self.db.execute(
            query=DELETE_USER_BY_ID_QUERY,
            values={"id": id},
        )
