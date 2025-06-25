from typing import (
    Any,
    Type,
    TypeVar,
    Optional
)

from sqlalchemy.exc import SQLAlchemyError
from src.core.db import db
from src.models.base import BaseModel


Model = TypeVar("Model", bound=BaseModel)


class BaseRepository:
    def __init__(self, model_class: Type[Model]):
        self.model_class = model_class

    def create(self, model: Model) -> tuple[Optional[Model], Optional[str]]:
        try:
            db.session.add(model)
            db.session.commit()

            return model, None
        except SQLAlchemyError as err:
            db.session.rollback()
            return None, str(err)

    def get_by_id(self, obj_id: int) -> tuple[Optional[Model], Optional[str]]:
        try:
            instance = db.session.get(self.model_class, obj_id)

            return instance, None

        except SQLAlchemyError as err:
            return None, str(err)

    def get_all(self) -> tuple[Optional[Model | list], Optional[str]]:
        try:
            list_of_instances = db.session.query(self.model_class).all()

            return list_of_instances, None

        except SQLAlchemyError as err:
            empty_list = []
            return empty_list, str(err)

    def update(self, obj_id: int, data: dict[str, Any]) -> tuple[Optional[Model], Optional[str]]:
        try:
            instance = db.session.get(self.model_class, obj_id)

            if not instance:
                return None, f"{self.model_class.__name__} not found"

            for attr, value in data.items():
                if hasattr(instance, attr):
                    setattr(instance, attr, value)

            db.session.commit()
            return instance, None

        except SQLAlchemyError as err:
            return None, str(err)

    def delete(self, obj_id: int) -> tuple[bool, Optional[str]]:
        try:
            instance = db.session.get(self.model_class, obj_id)

            if not instance:
                return False, f"{self.model_class.__name__} not found"

            db.session.delete(instance)
            db.session.commit()

            return True, None

        except SQLAlchemyError as err:
            db.session.rollback()
            return False, str(err)
