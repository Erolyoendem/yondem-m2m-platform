from fastapi import APIRouter, Depends, Query, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.database.session import get_db
from app.dependencies import get_language
from app.tools.shop_tools import ShopTools
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/mcp", tags=["MCP Tools"])


def get_shop_tools(db: AsyncSession = Depends(get_db)):
    return ShopTools(db)


@router.get("/search")
@limiter.limit("10/minute")
async def search_products(
    request: Request,
    q: str = Query(..., description="Search query"),
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools),
):
    return await shop_tools.search_products(q, lang)


@router.get("/product/{product_id}")
@limiter.limit("20/minute")
async def get_product(
    request: Request,
    product_id: str,
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools),
):
    return await shop_tools.get_product_details(product_id, lang)


@router.get("/compare")
@limiter.limit("5/minute")
async def compare_prices(
    request: Request,
    product: str = Query(..., description="Product name to compare"),
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools),
):
    return await shop_tools.compare_prices(product, lang)


@router.get("/deals")
@limiter.limit("15/minute")
async def get_deals(
    request: Request,
    category: Optional[str] = Query(None),
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools),
):
    return await shop_tools.get_deals(category, lang)


@router.get("/cashback/{shop_id}")
@limiter.limit("30/minute")
async def get_cashback(
    request: Request,
    shop_id: str,
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools),
):
    return await shop_tools.get_cashback_info(shop_id, lang)
