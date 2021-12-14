from typing import Optional

from pydantic import BaseModel, Field

from app.models.common import IDModelMixin


class Shop(IDModelMixin):
    name: str = Field(default='Unnamed', title='name of shop', max_length=100)
    description: str = Field(default='', title='description of shop')
    address: Optional[str] = Field(default=None, title='address of shop', max_length=400)
    website: str = Field(default='', title='website url of shop', max_length=400)
    rating: float = Field(default=0.0, title='rating by comment of shop', ge=0., le=5.0)

    def filter(
            self,
            name: Optional[str],
            address: Optional[str],
            website: Optional[str],
            lt_rating: Optional[float],
            gt_rating: Optional[float]
    ):

        if name is not None and name not in self.name:
            return False
        if address is not None and self.address != address:
            return False
        if website is not None and self.website != website:
            return False
        if lt_rating is not None and self.rating > lt_rating:
            return False
        if gt_rating is not None and self.rating < gt_rating:
            return False
        return True

class InsertShop(BaseModel):
    name: str = Field(default='Unnamed', title='name of shop', max_length=100)
    description: str = Field(default='', title='description of shop')
    address: Optional[str] = Field(default=None, title='address of shop', max_length=400)
    website: str = Field(default='', title='website url of shop', max_length=400)
    rating: float = Field(default=0.0, title='rating by comment of shop', ge=0., le=5.0)


class UpdateShop(BaseModel):
    name: Optional[str] = Field(default=None, title='name of shop', max_length=100)
    description: Optional[str] = Field(default=None, title='description of shop')
    address: Optional[str] = Field(default=None, title='address of shop', max_length=400)
    website: Optional[str] = Field(default=None, title='website url of shop', max_length=400)
    rating: Optional[float] = Field(default=None, title='rating by comment of shop', ge=0., le=5.0)
