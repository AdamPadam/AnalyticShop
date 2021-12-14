from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class Wishlist(IDModelMixin):
    user_id: UUID = Field(title='owner of wishlist')
    product_id: UUID = Field(title='product in wishlist')

    def filter(
            self,
            user_id: Optional[UUID],
            product_id: Optional[UUID]
    ):
        if user_id is not None and self.user_id != user_id:
            return False
        if product_id is not None and self.product_id != product_id:
            return False
        return True


class InsertWishlist(BaseModel):
    user_id: UUID = Field(title='owner of wishlist')
    product_id: UUID = Field(title='product in wishlist')
