from datetime import date
from typing import List, Optional
from uuid import UUID

from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.queries.users import *
from app.models.user import User
from .base import BaseRepository


class UsersRepository(BaseRepository):
    async def get_all(self) -> List[User]:
        data = await self.connection.fetch(GET_ALL_USERS)
        users = [User(**user) for user in data]

        return users

    async def create(
            self,
            username: str,
            password: str,
            first_name: Optional[str],
            last_name: Optional[str],
            birth_date: Optional[date]
    ) -> User:
        try:
            data = await self.connection.fetch(CREATE_USER, username, password, first_name, last_name, birth_date)
        except Exception as exec:
            raise EntityCreateError(f"Entity dose not created")
        user = User(**data[0])
        return user

    async def get_by_id(self, id: UUID) -> User:
        data = await self.connection.fetch(GET_BY_ID_USER, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        user = User(**data[0])
        return user

    async def update_by_id(
            self,
            id: UUID,
            username: str,
            password: str,
            first_name: Optional[str],
            last_name: Optional[str],
            birth_date: Optional[date]
    ) -> User:
        data = await self.connection.fetch(UPDATE_BY_ID_USER, id, username, password, first_name, last_name, birth_date)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        user = User(**data[0])
        return user

    async def delete_by_id(self, id: UUID) -> User:
        data = await self.connection.fetch(DELETE_BY_ID_USER, id)
        if not data:
            raise EntityDoesNotExistError(f"Entity with id: {id} does not exist")

        user = User(**data[0])
        return user
