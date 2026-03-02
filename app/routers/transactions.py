from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

from app.database.session import get_db
from app.models.transaction import Transaction
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/transactions", tags=["Transactions"])


@router.get("/")
@limiter.limit("10/minute")
async def list_transactions(
    request: Request,
    publisher_id: Optional[str] = None,
    advertiser_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
):
    stmt = select(Transaction).order_by(Transaction.created_at.desc())
    if publisher_id:
        stmt = stmt.where(Transaction.publisher_id == publisher_id)
    if advertiser_id:
        stmt = stmt.where(Transaction.advertiser_id == advertiser_id)

    result = await db.execute(stmt)
    transactions = result.scalars().all()

    return {
        "status": "success",
        "count": len(transactions),
        "transactions": [
            {
                "id": t.id,
                "publisher_id": t.publisher_id,
                "advertiser_id": t.advertiser_id,
                "product_price": t.product_price,
                "commission_amount": t.commission_amount,
                "platform_fee": t.platform_fee,
                "status": t.status,
                "created_at": t.created_at.isoformat() if t.created_at else None,
            }
            for t in transactions
        ],
    }


@router.get("/{transaction_id}")
@limiter.limit("10/minute")
async def get_transaction(
    request: Request,
    transaction_id: str,
    db: AsyncSession = Depends(get_db),
):
    result = await db.execute(
        select(Transaction).where(Transaction.id == transaction_id)
    )
    transaction = result.scalar_one_or_none()
    if not transaction:
        raise HTTPException(status_code=404, detail="Transaction not found")

    return {
        "status": "success",
        "transaction": {
            "id": transaction.id,
            "publisher_id": transaction.publisher_id,
            "advertiser_id": transaction.advertiser_id,
            "product_id": transaction.product_id,
            "contract_id": transaction.contract_id,
            "product_price": transaction.product_price,
            "commission_amount": transaction.commission_amount,
            "platform_fee": transaction.platform_fee,
            "status": transaction.status,
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None,
        },
    }
