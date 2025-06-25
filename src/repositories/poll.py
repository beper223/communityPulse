from typing import Optional

from sqlalchemy.exc import SQLAlchemyError

from src.core.db import db
from src.models import Poll, PollOption
from src.repositories.base import BaseRepository


class PollRepository(BaseRepository):
    def __init__(self):
        super().__init__(Poll)

    def create_with_options(
            self,
            poll_data: dict,
            poll_options: list[str]
    ) -> tuple[Optional[Poll], Optional[str]]:
        try:
            poll = Poll(**poll_data)

            for option in poll_options:
                option = PollOption(text=option)
                poll.options.append(option)

            db.session.add(poll)
            db.session.commit()
            db.session.refresh(poll)

            return poll, None

        except SQLAlchemyError as err:
            db.session.rollback()
            return None, str(err)
