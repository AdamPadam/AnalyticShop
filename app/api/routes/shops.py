from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.repositories.shops import ShopsRepository
from app.models.shop import Shop, InsertShop, UpdateShop

router = APIRouter()


@router.get("/", response_model=List[Shop])
async def get_all(
        name: Optional[str] = None,
        address: Optional[str] = None,
        website: Optional[str] = None,
        lt_rating: Optional[float] = None,
        gt_rating: Optional[float] = None,
        sorted_by: Optional[str] = None,
        reverse: bool = False,
        shops_repo: ShopsRepository = Depends(get_repository(ShopsRepository))
) -> List[Shop]:
    shops = await shops_repo.get_all()
    filtered_shops = []
    for shop in shops:
        is_fit = shop.filter(
            name=name,
            address=address,
            website=website,
            lt_rating=lt_rating,
            gt_rating=gt_rating
        )
        if is_fit:
            filtered_shops.append(shop)

    if sorted_by is not None and filtered_shops:
        print(filtered_shops[0].__dict__.keys())
        if sorted_by not in filtered_shops[0].__dict__.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str('Model Feedback has no attribute: ' + sorted_by))
        else:
            filtered_shops.sort(key=lambda shop: getattr(shop, sorted_by), reverse=reverse)

    return filtered_shops


@router.post("/", response_model=Shop, status_code=status.HTTP_201_CREATED)
async def create(
        shop_body: InsertShop = Body(..., embed=False),
        shops_repo: ShopsRepository = Depends(get_repository(ShopsRepository))
) -> Shop:
    try:
        name = shop_body.name
        description = shop_body.description
        address = shop_body.address
        website = shop_body.website
        rating = shop_body.rating

        shop = await shops_repo.create(
            name=name,
            description=description,
            address=address,
            website=website,
            rating=rating
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return shop


@router.get("/{id}", response_model=Shop)
async def get_by_id(
        id: UUID,
        shops_repo: ShopsRepository = Depends(get_repository(ShopsRepository))
) -> Shop:
    try:
        shop = await shops_repo.get_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return shop


@router.put("/{id}", response_model=Shop)
async def update(
        id: UUID,
        shop_body: UpdateShop = Body(..., embed=False),
        shops_repo: ShopsRepository = Depends(get_repository(ShopsRepository))
) -> Shop:
    try:
        shop = await shops_repo.get_by_id(id=id)

        name = shop_body.name
        description = shop_body.description
        address = shop_body.address
        website = shop_body.website
        rating = shop_body.rating

        if name is None:
            name = shop.name
        if description is None:
            description = shop.description
        if address is None:
            address = shop.address
        if website is None:
            website = shop.website
        if rating is None:
            rating = shop.rating
        updated_shop = await shops_repo.update_by_id(
            id=id,
            name=name,
            description=description,
            address=address,
            website=website,
            rating=rating
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return updated_shop


@router.delete("/{id}", response_model=Shop)
async def delete(
        id: UUID,
        shops_repo: ShopsRepository = Depends(get_repository(ShopsRepository))
) -> Shop:
    try:
        shop = await shops_repo.delete_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return shop
