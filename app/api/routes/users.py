from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.repositories.users import UsersRepository
from app.models.user import User, InsertUser, UpdateUser

router = APIRouter()


@router.get("/", response_model=List[User])
async def get_all(
        username: Optional[str] = None,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        birth_date: Optional[date] = None,
        sorted_by: Optional[str] = None,
        reverse: bool = False,
        users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> List[User]:
    users = await users_repo.get_all()
    filtered_users = []
    for user in users:
        is_fit = user.filter(
            username=username,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date
        )
        if is_fit:
            filtered_users.append(user)

    if sorted_by is not None and filtered_users:
        print(filtered_users[0].__dict__.keys())
        if sorted_by not in filtered_users[0].__dict__.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str('Model Feedback has no attribute: ' + sorted_by))
        else:
            filtered_users.sort(key=lambda user: getattr(user, sorted_by), reverse=reverse)

    return filtered_users


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
async def create(
        user_body: InsertUser = Body(..., embed=False),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> User:
    try:
        username = user_body.username
        password = user_body.password
        first_name = user_body.first_name
        last_name = user_body.last_name
        birth_date = user_body.birth_date

        user = await users_repo.create(
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return user


@router.get("/{id}", response_model=User)
async def get_by_id(
        id: UUID,
        users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> User:
    try:
        user = await users_repo.get_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return user


@router.put("/{id}", response_model=User)
async def update(
        id: UUID,
        user_body: UpdateUser = Body(..., embed=False),
        users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> User:
    try:
        user = await users_repo.get_by_id(id=id)

        username = user_body.username
        password = user_body.password
        first_name = user_body.first_name
        last_name = user_body.last_name
        birth_date = user_body.birth_date

        if username is None:
            username = user.username
        if password is None:
            password = user.password
        if first_name is None:
            first_name = user.first_name
        if last_name is None:
            last_name = user.last_name
        if birth_date is None:
            birth_date = user.birth_date

        updated_user = await users_repo.update_by_id(
            id=id,
            username=username,
            password=password,
            first_name=first_name,
            last_name=last_name,
            birth_date=birth_date
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return updated_user


@router.delete("/{id}", response_model=User)
async def delete(
        id: UUID,
        users_repo: UsersRepository = Depends(get_repository(UsersRepository))
) -> User:
    try:
        user = await users_repo.delete_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return user
