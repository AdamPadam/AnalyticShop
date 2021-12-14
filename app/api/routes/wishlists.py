from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, status, Body
from fastapi.exceptions import HTTPException

from app.api.dependencies.database import get_repository
from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.db.repositories.wishlists import WishlistsRepository
from app.models.wishlist import Wishlist, InsertWishlist

router = APIRouter()


@router.get("/", response_model=List[Wishlist])
async def get_all(
        user_id: Optional[UUID] = None,
        product_id: Optional[UUID] = None,
        sorted_by: Optional[str] = None,
        reverse: bool = False,
        wishlists_repo: WishlistsRepository = Depends(get_repository(WishlistsRepository))
) -> List[Wishlist]:
    wishlists = await wishlists_repo.get_all()
    filtered_wishlists = []
    for wishlist in wishlists:
        is_fit = wishlist.filter(
            user_id=user_id,
            product_id=product_id
        )
        if is_fit:
            filtered_wishlists.append(wishlist)

    if sorted_by is not None and filtered_wishlists:
        print(filtered_wishlists[0].__dict__.keys())
        if sorted_by not in filtered_wishlists[0].__dict__.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str('Model Feedback has no attribute: ' + sorted_by))
        else:
            filtered_wishlists.sort(key=lambda wishlist: getattr(wishlist, sorted_by), reverse=reverse)

    return filtered_wishlists


@router.post("/", response_model=Wishlist, status_code=status.HTTP_201_CREATED)
async def create(
        wishlist_body: InsertWishlist = Body(..., embed=False),
        wishlists_repo: WishlistsRepository = Depends(get_repository(WishlistsRepository))
) -> Wishlist:
    try:
        user_id = wishlist_body.user_id
        product_id = wishlist_body.product_id

        wishlist = await wishlists_repo.create(
            user_id=user_id,
            product_id=product_id
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return wishlist


@router.get("/{id}", response_model=Wishlist)
async def get_by_id(
        id: UUID,
        wishlists_repo: WishlistsRepository = Depends(get_repository(WishlistsRepository))
) -> Wishlist:
    try:
        wishlist = await wishlists_repo.get_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return wishlist


@router.delete("/{id}", response_model=Wishlist)
async def delete(
        id: UUID,
        wishlists_repo: WishlistsRepository = Depends(get_repository(WishlistsRepository))
) -> Wishlist:
    try:
        wishlist = await wishlists_repo.delete_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return wishlist
