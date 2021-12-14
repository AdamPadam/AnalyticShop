from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.repositories.groups import GroupsRepository
from app.models.group import Group, InsertGroup, UpdateGroup

router = APIRouter()


@router.get("/", response_model=List[Group])
async def get_all(
        name: Optional[str],
        permission_type: Optional[str],
        sorted_by: Optional[str] = None,
        reverse: bool = False,
        groups_repo: GroupsRepository = Depends(get_repository(GroupsRepository))
) -> List[Group]:
    groups = await groups_repo.get_all()
    filtered_groups = []
    for group in groups:
        is_fit = group.filter(
            name=name,
            permission_type=permission_type
        )
        if is_fit:
            filtered_groups.append(group)

    if sorted_by is not None and filtered_groups:
        print(filtered_groups[0].__dict__.keys())
        if sorted_by not in filtered_groups[0].__dict__.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str('Model Feedback has no attribute: ' + sorted_by))
        else:
            filtered_groups.sort(key=lambda group: getattr(group, sorted_by), reverse=reverse)

    return filtered_groups


@router.post("/", response_model=Group, status_code=status.HTTP_201_CREATED)
async def create(
        group_body: InsertGroup = Body(..., embed=False),
        groups_repo: GroupsRepository = Depends(get_repository(GroupsRepository))
) -> Group:
    try:
        name = group_body.name
        permission_type = group_body.permission_type

        group = await groups_repo.create(
            name=name,
            permission_type=permission_type
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return group


@router.get("/{id}", response_model=Group)
async def get_by_id(
        id: UUID,
        groups_repo: GroupsRepository = Depends(get_repository(GroupsRepository))
) -> Group:
    try:
        group = await groups_repo.get_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return group


@router.put("/{id}", response_model=Group)
async def update(
        id: UUID,
        group_body: UpdateGroup = Body(..., embed=False),
        groups_repo: GroupsRepository = Depends(get_repository(GroupsRepository))
) -> Group:
    try:
        group = await groups_repo.get_by_id(id=id)

        name = group_body.name
        permission_type = group_body.permission_type

        if name is None:
            name = group.name
        if permission_type is None:
            permission_type = group.permission_type

        updated_group = await groups_repo.update_by_id(id=id, name=name, permission_type=permission_type)
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return updated_group


@router.delete("/{id}", response_model=Group)
async def delete(
        id: UUID,
        groups_repo: GroupsRepository = Depends(get_repository(GroupsRepository))
) -> Group:
    try:
        group = await groups_repo.delete_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return group
