from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional
import uuid

from app.database.session import get_db
from app.models.bid import Bid
from app.models.agent import Agent, AgentType
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/bidding", tags=["Bidding"])

class BidCreate(BaseModel):
    product_category: str
    target_product: Optional[str] = None
    commission_rate: float = 0.10
    max_cpc: float = 0.50
    daily_budget: float = 100.0

@router.post("/{advertiser_id}/create")
@limiter.limit("5/minute")
async def create_bid(
    request: Request,
    advertiser_id: str,
    bid_data: BidCreate,
    db: Session = Depends(get_db)
):
    """Advertiser erstellt ein Bidding-Angebot"""
    agent = db.query(Agent).filter(Agent.id == advertiser_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.type != AgentType.ADVERTISER:
        raise HTTPException(status_code=403, detail="Only Advertiser agents can create bids")
    
    bid = Bid(
        id=str(uuid.uuid4()),
        advertiser_id=advertiser_id,
        product_category=bid_data.product_category,
        target_product=bid_data.target_product,
        commission_rate=bid_data.commission_rate,
        max_cpc=bid_data.max_cpc,
        daily_budget=bid_data.daily_budget
    )
    
    db.add(bid)
    db.commit()
    db.refresh(bid)
    
    return {
        "status": "success",
        "bid_id": bid.id,
        "message": f"Bid created for category: {bid_data.product_category}"
    }

@router.get("/")
@limiter.limit("10/minute")
async def list_bids(
    request: Request,
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Liste alle aktiven Bids (optional nach Kategorie gefiltert)"""
    query = db.query(Bid).filter(Bid.is_active == 1)
    
    if category:
        query = query.filter(Bid.product_category == category)
    
    bids = query.order_by(Bid.commission_rate.desc()).all()
    
    return {
        "status": "success",
        "count": len(bids),
        "bids": [
            {
                "id": b.id,
                "advertiser_id": b.advertiser_id,
                "category": b.product_category,
                "target": b.target_product,
                "commission": f"{b.commission_rate*100}%",
                "max_cpc": b.max_cpc,
                "daily_budget": b.daily_budget
            }
            for b in bids
        ]
    }

@router.post("/{bid_id}/select")
@limiter.limit("10/minute")
async def select_best_bid(
    request: Request,
    bid_id: str,
    publisher_id: str,
    db: Session = Depends(get_db)
):
    """Publisher wählt ein Bid aus (für spätere Automatisierung)"""
    bid = db.query(Bid).filter(Bid.id == bid_id, Bid.is_active == 1).first()
    if not bid:
        raise HTTPException(status_code=404, detail="Bid not found or inactive")
    
    return {
        "status": "success",
        "selected_bid": bid_id,
        "publisher": publisher_id,
        "commission_rate": bid.commission_rate,
        "message": "Bid selected for transaction"
    }
