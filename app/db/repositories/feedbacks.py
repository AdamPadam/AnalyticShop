from typing import List, Optional
from uuid import UUID

from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.queries.feedbacks import *
from app.models.feedback import Feedback
from .base import BaseRepository


class FeedbacksRepository(BaseRepository):
    async def get_all(self) -> List[Feedback]:
        data = await self.connection.fetch(GET_ALL_FEEDBACKS)
        feedbacks = [Feedback(**feedback) for feedback in data]

        return feedbacks

    async def create(
            self,
            title: str,
            positive_msg: str,
            negative_msg: str,
            message: str,
            user_id: UUID,
            product_id: Optional[UUID] = None,
            shop_id: Optional[UUID] = None
    ) -> Feedback:
        try:
            data = await self.connection.fetch(CREATE_FEEDBACK, title, positive_msg, negative_msg, message, user_id,
                                               product_id, shop_id)
        except Exception as exc:
            raise EntityCreateError(f"Entity dose not created")

        feedback = Feedback(**data[0])
        return feedback

    async def get_by_id(self, id: UUID) -> Feedback:
        data = await self.connection.fetch(GET_BY_ID_FEEDBACK, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        feedback = Feedback(**data[0])
        return feedback

    async def update_by_id(
            self,
            id: UUID,
            title: str,
            positive_msg: str,
            negative_msg: str,
            message: str
    ) -> Feedback:
        data = await self.connection.fetch(UPDATE_BY_ID_FEEDBACK, id, title, positive_msg, negative_msg, message)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        feedback = Feedback(**data[0])
        return feedback

    async def delete_by_id(self, id: UUID) -> Feedback:
        data = await self.connection.fetch(DELETE_BY_ID_FEEDBACK, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        feedback = Feedback(**data[0])
        return feedback
