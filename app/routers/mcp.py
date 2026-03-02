from fastapi import APIRouter, Depends, Query, HTTPException, Request
from sqlalchemy.orm import Session
from typing import Optional

from app.tools.shop_tools import ShopTools
from app.dependencies import get_language
from app.database.session import get_db
from app.core.rate_limiter import limiter
from app.schemas.mcp import (
    SearchProductsResponse,
    ProductDetailsResponse,
    PriceComparisonResponse,
    DealsResponse,
    CashbackInfoResponse
)

router = APIRouter(prefix="/mcp", tags=["MCP Tools"])

def get_shop_tools(db: Session = Depends(get_db)):
    return ShopTools(db)

@router.get("/search", response_model=SearchProductsResponse)
@limiter.limit("10/minute")
async def search_products(
    request: Request,
    q: str = Query(..., description="Search query for products"),
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools)
):
    """Search for products across all shops
    
    - **q**: Search term (searches in name and description)
    - Returns list of matching products with shop information
    """
    return await shop_tools.search_products(q, lang)

@router.get("/product/{product_id}", response_model=ProductDetailsResponse)
@limiter.limit("20/minute")
async def get_product(
    request: Request,
    product_id: str,
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools)
):
    """Get detailed information about a specific product
    
    - **product_id**: UUID of the product
    - Returns full product details including URL and shop
    """
    return await shop_tools.get_product_details(product_id, lang)

@router.get("/compare", response_model=PriceComparisonResponse)
@limiter.limit("5/minute")
async def compare_prices(
    request: Request,
    product: str = Query(..., description="Product name to compare prices"),
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools)
):
    """Compare prices across different shops
    
    - **product**: Product name to search for
    - Returns price comparison with cashback info per shop
    """
    return await shop_tools.compare_prices(product, lang)

@router.get("/deals", response_model=DealsResponse)
@limiter.limit("15/minute")
async def get_deals(
    request: Request,
    category: Optional[str] = Query(None, description="Filter by deal category"),
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools)
):
    """Get current deals and offers
    
    - **category**: Optional category filter
    - Returns list of active deals with discount codes
    """
    return await shop_tools.get_deals(category, lang)

@router.get("/cashback/{shop_id}", response_model=CashbackInfoResponse)
@limiter.limit("30/minute")
async def get_cashback(
    request: Request,
    shop_id: str,
    lang: str = Depends(get_language),
    shop_tools: ShopTools = Depends(get_shop_tools)
):
    """Get cashback information for a specific shop
    
    - **shop_id**: UUID of the shop
    - Returns cashback percentage and fixed amounts
    """
    return await shop_tools.get_cashback_info(shop_id, lang)
