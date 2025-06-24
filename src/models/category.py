from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import BaseModel
from src.core.app_runner import db

class Category(BaseModel):
    __tablename__ = "categories"

    name: Mapped[str] = mapped_column(
        db.String(120),
        nullable=False
    )

    # Relations

    polls: Mapped[list["Poll"]] = relationship(
        "Poll",
        back_populates="category",
        cascade="all, delete-orphan"
    )