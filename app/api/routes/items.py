from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.repositories.items import ItemsRepository
from app.models.item import Item, InsertItem, UpdateItem

router = APIRouter()


@router.get("/", response_model=List[Item])
async def get_all(
        product_id: Optional[UUID] = None,
        shop_id: Optional[UUID] = None,
        not_zero_quantity: bool = False,
        not_zero_discount_percent: bool = False,
        gt_discount_percent: Optional[int] = None,
        lt_price: Optional[float] = None,
        gt_price: Optional[float] = None,
        sorted_by: Optional[str] = None,
        reverse: bool = False,
        items_repo: ItemsRepository = Depends(get_repository(ItemsRepository))
) -> List[Item]:
    items = await items_repo.get_all()
    filtered_items = []
    for item in items:
        is_fit = item.filter(
            product_id=product_id,
            shop_id=shop_id,
            not_zero_quantity=not_zero_quantity,
            not_zero_discount_percent=not_zero_discount_percent,
            gt_discount_percent=gt_discount_percent,
            lt_price=lt_price,
            gt_price=gt_price
        )
        if is_fit:
            filtered_items.append(item)

    if sorted_by is not None and filtered_items:
        print(filtered_items[0].__dict__.keys())
        if sorted_by not in filtered_items[0].__dict__.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str('Model Feedback has no attribute: ' + sorted_by))
        else:
            filtered_items.sort(key=lambda item: getattr(item, sorted_by), reverse=reverse)

    return filtered_items


@router.post("/", response_model=Item, status_code=status.HTTP_201_CREATED)
async def create(
        item_body: InsertItem = Body(..., embed=False),
        items_repo: ItemsRepository = Depends(get_repository(ItemsRepository))
) -> Item:
    try:
        title = item_body.title
        positive_msg = item_body.positive_msg
        negative_msg = item_body.negative_msg
        message = item_body.message
        user_id = item_body.user_id
        product_id = item_body.product_id
        shop_id = item_body.shop_id

        item = await items_repo.create(
            title=title,
            positive_msg=positive_msg,
            negative_msg=negative_msg,
            message=message,
            user_id=user_id,
            product_id=product_id,
            shop_id=shop_id
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return item


@router.get("/{id}", response_model=Item)
async def get_by_id(
        id: UUID,
        items_repo: ItemsRepository = Depends(get_repository(ItemsRepository))
) -> Item:
    try:
        item = await items_repo.get_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return item


@router.put("/{id}", response_model=Item)
async def update(
        id: UUID,
        item_body: UpdateItem = Body(..., embed=False),
        items_repo: ItemsRepository = Depends(get_repository(ItemsRepository))
) -> Item:
    try:
        item = await items_repo.get_by_id(id=id)

        title = item_body.title
        positive_msg = item_body.positive_msg
        negative_msg = item_body.negative_msg
        message = item_body.message

        if title is None:
            title = item.title
        if positive_msg is None:
            positive_msg = item.positive_msg
        if negative_msg is None:
            negative_msg = item.negative_msg
        if message is None:
            message = item.message
        updated_item = await items_repo.update_by_id(id=id, title=title, positive_msg=positive_msg,
                                                     negative_msg=negative_msg, message=message)
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return updated_item


@router.delete("/{id}", response_model=Item)
async def delete(
        id: UUID,
        items_repo: ItemsRepository = Depends(get_repository(ItemsRepository))
) -> Item:
    try:
        item = await items_repo.delete_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return item
