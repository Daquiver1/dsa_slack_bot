"""User Models."""


from src.models.core import CoreModel, DateTimeModelMixin, IDModelMixin


class UserBase(CoreModel):
    """User Base Model."""

    first_name: str
    last_name: str
    slack_id: str


class CreateUserClient(UserBase):
    """User Model used in creating a new user."""

    pass


class UserInDB(UserBase, IDModelMixin, DateTimeModelMixin):
    """User coming from DB."""

    pass


class UserPublic(UserBase, DateTimeModelMixin):
    """Public user model."""

    pass
