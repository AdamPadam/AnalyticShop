from typing import List, Optional
from uuid import UUID

from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.queries.shops import *
from app.models.shop import Shop
from .base import BaseRepository


class ShopsRepository(BaseRepository):
    async def get_all(self) -> List[Shop]:
        data = await self.connection.fetch(GET_ALL_SHOPS)
        shops = [Shop(**shop) for shop in data]

        return shops

    async def create(
            self,
            name: str,
            description: str,
            address: Optional[str],
            website: str,
            rating: float
    ) -> Shop:
        try:
            data = await self.connection.fetch(CREATE_SHOP, name, description, address, website, rating)
        except Exception as exec:
            raise EntityCreateError(f"Entity dose not created")

        shop = Shop(**data[0])
        return shop

    async def get_by_id(self, id: UUID) -> Shop:
        data = await self.connection.fetch(GET_BY_ID_SHOP, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        shop = Shop(**data[0])
        return shop

    async def update_by_id(
            self,
            id: UUID,
            name: str,
            description: str,
            address: Optional[str],
            website: str,
            rating: float
    ) -> Shop:
        data = await self.connection.fetch(UPDATE_BY_ID_SHOP, id, name, description, address, website, rating)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        shop = Shop(**data[0])
        return shop

    async def delete_by_id(self, id: UUID) -> Shop:
        data = await self.connection.fetch(DELETE_BY_ID_SHOP, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        shop = Shop(**data[0])
        return shop
