from typing import Optional
from uuid import UUID
from datetime import date, datetime

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class Feedback(IDModelMixin):
    title: str = Field(default='Untitled', title='title of feedback', max_length=50)
    positive_msg: str = Field(default='', title='message about positive moments', max_length=200)
    negative_msg: str = Field(default='', title='message about negative moments', max_length=200)
    message: str = Field(default='', title='extra message', max_length=400)
    user_id: UUID = Field(title='owner of feedback')
    product_id: Optional[UUID] = Field(default=None, title='target product')
    shop_id: Optional[UUID] = Field(default=None, title='target shop')

    def filter(
            self,
            title: Optional[str],
            user_id: Optional[UUID],
            product_id: Optional[UUID],
            only_products: bool,
            shop_id: Optional[UUID],
            only_shops: bool,
            date: Optional[date],
            before_date: Optional[date],
            after_date: Optional[date]
    ):
        
        if title is not None and title not in self.title:
            return False
        if user_id is not None and self.user_id != user_id:
            return False
        if only_products and self.product_id is None:
            return False
        if product_id is not None and self.product_id != product_id:
            return False
        if only_shops and self.shop_id is None:
            return False
        if shop_id is not None and self.shop_id != shop_id:
            return False
        if date is not None and self.created != datetime(date):
            return False
        if before_date is not None and self.created > datetime(before_date):
            return False
        if after_date is not None and self.created < datetime(after_date):
            return False
        return True

class InsertFeedback(BaseModel):
    title: str = Field(default='Untitled', title='title of feedback', max_length=50)
    positive_msg: str = Field(default='', title='message about positive moments', max_length=200)
    negative_msg: str = Field(default='', title='message about negative moments', max_length=200)
    message: str = Field(default='', title='extra message', max_length=400)
    user_id: UUID = Field(title='owner of feedback')
    product_id: Optional[UUID] = Field(default=None, title='target product')
    shop_id: Optional[UUID] = Field(default=None, title='target shop')


class UpdateFeedback(BaseModel):
    title: Optional[str] = Field(default=None, title='title of feedback', max_length=50)
    positive_msg: Optional[str] = Field(default=None, title='message about positive moments', max_length=200)
    negative_msg: Optional[str] = Field(default=None, title='message about negative moments', max_length=200)
    message: Optional[str] = Field(default=None, title='extra message', max_length=400)
