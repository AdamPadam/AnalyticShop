from typing import List, Optional
from uuid import UUID

from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.queries.groups import *
from app.models.group import Group
from .base import BaseRepository


class GroupsRepository(BaseRepository):
    async def get_all(self) -> List[Group]:
        data = await self.connection.fetch(GET_ALL_GROUPS)
        groups = [Group(**group) for group in data]

        return groups

    async def create(
            self,
            name: str,
            permission_type: int
    ) -> Group:
        try:
            data = await self.connection.fetch(CREATE_GROUP, name, permission_type)
        except Exception as exec:
            raise EntityCreateError(f"Entity dose not created")

        group = Group(**data[0])
        return group

    async def get_by_id(self, id: UUID) -> Group:
        data = await self.connection.fetch(GET_BY_ID_GROUP, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        group = Group(**data[0])
        return group

    async def update_by_id(
            self,
            id: UUID,
            name: str,
            permission_type: int
    ) -> Group:
        data = await self.connection.fetch(UPDATE_BY_ID_GROUP, id, name, permission_type)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        group = Group(**data[0])
        return group

    async def delete_by_id(self, id: UUID) -> Group:
        data = await self.connection.fetch(DELETE_BY_ID_GROUP, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        group = Group(**data[0])
        return group
