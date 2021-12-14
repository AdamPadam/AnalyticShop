import logging
from datetime import datetime
from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Query, Depends, status, Response, Body
from fastapi.exceptions import HTTPException

from app.models.product import Product, InsertProduct, UpdateProduct
from app.db.errors.common import EntityDoesNotExistError, EntityCreateError
from app.api.dependencies.database import get_repository
from app.db.repositories.products import ProductsRepository

router = APIRouter()


@router.get("/", response_model=List[Product])
async def get_all(
        name: Optional[str] = None,
        code: Optional[str] = None,
        lt_rating: Optional[float] = None,
        gt_rating: Optional[float] = None,
        category: Optional[str] = None,
        sorted_by: Optional[str] = None,
        reverse: bool = False,
        products_repo: ProductsRepository = Depends(get_repository(ProductsRepository))
) -> List[Product]:
    products = await products_repo.get_all()
    filtered_products = []
    for product in products:
        is_fit = product.filter(
            name=name,
            code=code,
            lt_rating=lt_rating,
            gt_rating=gt_rating,
            category=category
        )
        if is_fit:
            filtered_products.append(product)

    if sorted_by is not None and filtered_products:
        print(filtered_products[0].__dict__.keys())
        if sorted_by not in filtered_products[0].__dict__.keys():
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail=str('Model Feedback has no attribute: ' + sorted_by))
        else:
            filtered_products.sort(key=lambda product: getattr(product, sorted_by), reverse=reverse)

    return filtered_products


@router.post("/", response_model=Product, status_code=status.HTTP_201_CREATED)
async def create(
        product_body: InsertProduct = Body(..., embed=False),
        products_repo: ProductsRepository = Depends(get_repository(ProductsRepository))
) -> Product:
    try:
        name = product_body.name
        description = product_body.description
        code = product_body.code
        characteristic = product_body.characteristic
        rating = product_body.rating
        category = product_body.category

        product = await products_repo.create(
            name=name,
            description=description,
            code=code,
            characteristic=characteristic,
            rating=rating,
            category=category
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return product


@router.get("/{id}", response_model=Product)
async def get_by_id(
        id: UUID,
        products_repo: ProductsRepository = Depends(get_repository(ProductsRepository))
) -> Product:
    try:
        product = await products_repo.get_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return product


@router.put("/{id}", response_model=Product)
async def update(
        id: UUID,
        product_body: UpdateProduct = Body(..., embed=False),
        products_repo: ProductsRepository = Depends(get_repository(ProductsRepository))
) -> Product:
    try:
        product = await products_repo.get_by_id(id=id)

        name = product_body.name
        description = product_body.description
        code = product_body.code
        characteristic = product_body.characteristic
        rating = product_body.rating
        category = product_body.category

        if name is None:
            name = product.name
        if description is None:
            description = product.description
        if code is None:
            code = product.code
        if characteristic is None:
            characteristic = product.characteristic
        if rating is None:
            rating = product.rating
        if category is None:
            category = product.category

        updated_product = await products_repo.update_by_id(
            id=id,
            name=name,
            description=description,
            code=code,
            characteristic=characteristic,
            rating=rating,
            category=category
        )
    except EntityCreateError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    return updated_product


@router.delete("/{id}", response_model=Product)
async def delete(
        id: UUID,
        products_repo: ProductsRepository = Depends(get_repository(ProductsRepository))
) -> Product:
    try:
        product = await products_repo.delete_by_id(id)
    except EntityDoesNotExistError as exc:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(exc))
    return product
