from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class Item(IDModelMixin):
    product_id: UUID = Field(title='product of position')
    shop_id: UUID = Field(title='shop of position')
    quantity: int = Field(default=0, title='quantity of products in shop', ge=0)
    discount_percent: int = Field(default=0, title='discount in percent of product in shop', ge=0, le=100)
    price: float = Field(default=1.0, title='price of product in shop', gt=0.0)

    def filter(
            self,
            product_id: Optional[UUID],
            shop_id: Optional[UUID],
            not_zero_quantity: bool,
            not_zero_discount_percent: bool,
            gt_discount_percent: Optional[int],
            lt_price: Optional[float],
            gt_price: Optional[float]
    ):
        if product_id is not None and self.product_id != product_id:
            return False
        if shop_id is not None and self.shop_id != shop_id:
            return False
        if not_zero_quantity and self.quantity == 0:
            return False
        if not_zero_discount_percent and self.discount_percent == 0:
            return False
        if gt_discount_percent is not None and self.discount_percent < gt_discount_percent:
            return False
        if lt_price is not None and self.price > lt_price:
            return False
        if gt_price is not None and self.price < gt_price:
            return False
        return True


class InsertItem(BaseModel):
    product_id: UUID = Field(title='product of position')
    shop_id: UUID = Field(title='shop of position')
    quantity: int = Field(default=0, title='quantity of products in shop', ge=0)
    discount_percent: int = Field(default=0, title='discount in percent of product in shop', ge=0, le=100)
    price: float = Field(default=1.0, title='price of product in shop', gt=0.0)


class UpdateItem(BaseModel):
    quantity: Optional[int] = Field(default=None, title='quantity of products in shop')
    discount_percent: Optional[int] = Field(default=None, title='discount in percent of product in shop')
    price: Optional[float] = Field(default=None, title='price of product in shop')
