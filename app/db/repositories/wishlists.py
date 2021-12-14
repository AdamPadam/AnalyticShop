from typing import List
from uuid import UUID

from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.queries.wishlists import *
from app.models.wishlist import Wishlist
from .base import BaseRepository


class WishlistsRepository(BaseRepository):
    async def get_all(self) -> List[Wishlist]:
        data = await self.connection.fetch(GET_ALL_WISHLISTS)
        wishlist = [Wishlist(**wishlist) for wishlist in data]

        return wishlist

    async def create(
            self,
            user_id: UUID,
            product_id: UUID
    ) -> Wishlist:
        try:
            data = await self.connection.fetch(CREATE_WISHLIST, user_id, product_id)
        except Exception as exec:
            raise EntityCreateError(f"Entity dose not created")

        wishlist = Wishlist(**data[0])
        return wishlist

    async def get_by_id(self, id: UUID) -> Wishlist:
        data = await self.connection.fetch(GET_BY_ID_WISHLIST, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        wishlist = Wishlist(**data[0])
        return wishlist

    async def update_by_id(
            self,
            user_id: UUID,
            product_id: UUID
    ) -> Wishlist:
        data = await self.connection.fetch(UPDATE_BY_ID_WISHLIST, id, user_id, product_id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        wishlist = Wishlist(**data[0])
        return wishlist

    async def delete_by_id(self, id: UUID) -> Wishlist:
        data = await self.connection.fetch(DELETE_BY_ID_WISHLIST, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        wishlist = Wishlist(**data[0])
        return wishlist
