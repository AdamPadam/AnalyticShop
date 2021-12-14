from typing import Optional

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class Product(IDModelMixin):
    name: str = Field(default='Unnamed', title='name of product', max_length=100)
    description: str = Field(default='', title='description of product')
    code: str = Field(default='', title='code of product', max_length=50)
    characteristic: str = Field(default='{}', title='characteristic of product')
    rating: float = Field(default=0.0, title='rating by comment of product', ge=0., le=5.0)
    category: str = Field(default='Uncategorized', title='category of product', max_length=50)

    def filter(
            self,
            name: Optional[str],
            code: Optional[str],
            lt_rating: Optional[float],
            gt_rating: Optional[float],
            category: Optional[str]
    ):
        if name is not None and name not in self.name:
            return False
        if code is not None and self.code != code:
            return False
        if category is not None and category in self.category:
            return False
        if lt_rating is not None and self.rating > lt_rating:
            return False
        if gt_rating is not None and self.rating < gt_rating:
            return False
        return True


class InsertProduct(BaseModel):
    name: str = Field(default='Unnamed', title='name of product', max_length=100)
    description: str = Field(default='', title='description of product')
    code: str = Field(default='', title='code of product', max_length=50)
    characteristic: str = Field(default='{}', title='characteristic of product')
    rating: float = Field(default=0.0, title='rating by comment of product', ge=0., le=5.0)
    category: str = Field(default='Uncategorized', title='category of product', max_length=50)


class UpdateProduct(BaseModel):
    name: Optional[str] = Field(default=None, title='name of product')
    description: Optional[str] = Field(default=None, title='description of product')
    code: Optional[str] = Field(default=None, title='code of product')
    characteristic: Optional[str] = Field(default=None, title='characteristic of product')
    rating: Optional[float] = Field(default=None, title='rating by comment of product')
    category: Optional[str] = Field(default=None, title='category of product')
