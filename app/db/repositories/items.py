from typing import List, Optional
from uuid import UUID

from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.queries.items import *
from app.models.item import Item
from .base import BaseRepository


class ItemsRepository(BaseRepository):
    async def get_all(self) -> List[Item]:
        data = await self.connection.fetch(GET_ALL_ITEMS)
        items = [Item(**item) for item in data]

        return items

    async def create(
            self,
            product_id: UUID,
            shop_id: UUID,
            quantity: int,
            discount_percent: int,
            price: float
    ) -> Item:
        try:
            data = await self.connection.fetch(CREATE_ITEM, product_id, shop_id, quantity, discount_percent, price)
        except Exception as exec:
            raise EntityCreateError(f"Entity dose not created")

        item = Item(**data[0])
        return item

    async def get_by_id(self, id: UUID) -> Item:
        data = await self.connection.fetch(GET_BY_ID_ITEM, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        item = Item(**data[0])
        return item

    async def update_by_id(
            self,
            id: UUID,
            product_id: UUID,
            shop_id: UUID,
            quantity: int,
            discount_percent: int,
            price: float
    ) -> Item:
        data = await self.connection.fetch(UPDATE_BY_ID_ITEM, id, product_id, shop_id, quantity, discount_percent,
                                           price)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        item = Item(**data[0])
        return item

    async def delete_by_id(self, id: UUID) -> Item:
        data = await self.connection.fetch(DELETE_BY_ID_ITEM, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        item = Item(**data[0])
        return item
