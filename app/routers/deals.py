from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
import uuid

from app.database.session import get_db
from app.models.deal import Deal
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/deals", tags=["Deals"])


class DealCreate(BaseModel):
    title: str
    discount_value: Optional[float] = None
    discount_type: Optional[str] = None
    code: Optional[str] = None
    shop_id: int
    product_id: Optional[int] = None


@router.get("/")
@limiter.limit("30/minute")
async def list_deals(
    request: Request,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Deal).where(Deal.is_active == True).order_by(Deal.created_at.desc())
    )
    deals = result.scalars().all()
    return {
        "status": "success",
        "count": len(deals),
        "deals": [
            {
                "id": d.id,
                "title": d.title,
                "discount_value": d.discount_value,
                "discount_type": d.discount_type,
                "code": d.code,
                "shop_id": d.shop_id,
            }
            for d in deals
        ],
    }


@router.get("/{deal_id}")
@limiter.limit("60/minute")
async def get_deal(
    request: Request,
    deal_id: int,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(select(Deal).where(Deal.id == deal_id))
    deal = result.scalar_one_or_none()
    if not deal:
        raise HTTPException(status_code=404, detail=f"Deal {deal_id} not found")
    return {
        "status": "success",
        "deal": {
            "id": deal.id,
            "title": deal.title,
            "discount_value": deal.discount_value,
            "discount_type": deal.discount_type,
            "code": deal.code,
            "shop_id": deal.shop_id,
        },
    }


@router.post("/")
@limiter.limit("10/minute")
async def create_deal(
    request: Request,
    deal_data: DealCreate,
    db: AsyncSession = Depends(get_db),
):
    deal = Deal(
        title=deal_data.title,
        discount_value=deal_data.discount_value,
        discount_type=deal_data.discount_type,
        code=deal_data.code,
        shop_id=deal_data.shop_id,
        product_id=deal_data.product_id,
    )
    db.add(deal)
    await db.commit()
    await db.refresh(deal)
    return {"status": "success", "deal_id": deal.id, "title": deal.title}
