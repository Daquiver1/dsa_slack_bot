"""Leetcode update model."""
from datetime import date
from src.models.core import CoreModel, DateTimeModelMixin, IDModelMixin


class LeetcodeUpdateBase(CoreModel):
    """Leetcode Update Base Model."""

    leetcode_update: int
    posters_slack_id: str
    date: date


class CreateLeetcodeUpdateClient(LeetcodeUpdateBase):
    """Update Model used in creating a new leetcode update."""

    pass


class LeetcodeUpdateInDB(LeetcodeUpdateBase, IDModelMixin, DateTimeModelMixin):
    """Leetcode Update coming from DB."""

    pass


class LeetcodeUpdatePublic(LeetcodeUpdateBase, DateTimeModelMixin):
    """Public leetcode update model."""

    pass
