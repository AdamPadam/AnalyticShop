from fastapi import APIRouter

from app.api.routes import products
from app.api.routes import shops
from app.api.routes import items
from app.api.routes import users
from app.api.routes import feedbacks
from app.api.routes import wishlists
from app.api.routes import groups

router = APIRouter()

router.include_router(products.router, tags=["Products"], prefix="/products")

router.include_router(shops.router, tags=["Shops"], prefix="/shops")

router.include_router(items.router, tags=["Items"], prefix="/items")

router.include_router(users.router, tags=["Users"], prefix="/users")

router.include_router(feedbacks.router, tags=["Feedbacks"], prefix="/feedbacks")

router.include_router(wishlists.router, tags=["Wishlists"], prefix="/wishlists")

router.include_router(groups.router, tags=["Groups"], prefix="/groups")
