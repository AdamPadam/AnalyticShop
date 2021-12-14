from typing import List, Optional
from uuid import UUID

from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.queries.products import *
from app.models.product import Product
from .base import BaseRepository


class ProductsRepository(BaseRepository):
    async def get_all(self) -> List[Product]:
        data = await self.connection.fetch(GET_ALL_PRODUCTS)
        products = [Product(**product) for product in data]

        return products

    async def create(
            self,
            name: str,
            description: str,
            code: str,
            characteristic: dict,
            rating: float,
            category: str
    ) -> Product:
        try:
            data = await self.connection.fetch(CREATE_PRODUCT, name, description, code, characteristic, rating,
                                               category)
        except Exception as exec:
            raise EntityCreateError(f"Entity dose not created")

        product = Product(**data[0])
        return product

    async def get_by_id(self, id: UUID) -> Product:
        data = await self.connection.fetch(GET_BY_ID_PRODUCT, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        product = Product(**data[0])
        return product

    async def update_by_id(
            self,
            id: UUID,
            name: str,
            description: str,
            code: str,
            characteristic: dict,
            rating: float,
            category: str
    ) -> Product:
        data = await self.connection.fetch(UPDATE_BY_ID_PRODUCT, id, name, description, code, characteristic, rating,
                                           category)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        product = Product(**data[0])
        return product

    async def delete_by_id(self, id: UUID) -> Product:
        data = await self.connection.fetch(DELETE_BY_ID_PRODUCT, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        product = Product(**data[0])
        return product
