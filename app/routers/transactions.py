from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid

from app.database.session import get_db
from app.models.transaction import Transaction
from app.models.agent import Agent
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/transactions", tags=["Transactions"])

class TransactionResponse(BaseModel):
    id: str
    publisher_id: str
    advertiser_id: str
    product_price: float
    commission_amount: float
    status: str
    created_at: str
    
    class Config:
        orm_mode = True

@router.get("/")
@limiter.limit("10/minute")
async def list_transactions(
    request: Request,
    publisher_id: Optional[str] = None,
    advertiser_id: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Liste alle Transaktionen (optional gefiltert)"""
    query = db.query(Transaction)
    
    if publisher_id:
        query = query.filter(Transaction.publisher_id == publisher_id)
    if advertiser_id:
        query = query.filter(Transaction.advertiser_id == advertiser_id)
    
    transactions = query.order_by(Transaction.created_at.desc()).all()
    
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
                "created_at": t.created_at.isoformat() if t.created_at else None
            }
            for t in transactions
        ]
    }

@router.get("/{transaction_id}")
@limiter.limit("10/minute")
async def get_transaction(
    request: Request,
    transaction_id: str,
    db: Session = Depends(get_db)
):
    """Details einer einzelnen Transaktion"""
    transaction = db.query(Transaction).filter(Transaction.id == transaction_id).first()
    
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
            "created_at": transaction.created_at.isoformat() if transaction.created_at else None
        }
    }
