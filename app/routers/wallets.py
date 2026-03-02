from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database.session import get_db
from app.models.wallet import Wallet, WalletType
from app.models.agent import Agent
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/wallets", tags=["Wallets"])

class WalletCreate(BaseModel):
    address: str
    wallet_type: str = "polygon"

@router.post("/{agent_id}/create")
@limiter.limit("3/minute")
async def create_wallet(
    request: Request,
    agent_id: str,
    wallet_data: WalletCreate,
    db: Session = Depends(get_db)
):
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    existing = db.query(Wallet).filter(Wallet.agent_id == agent_id).first()
    if existing:
        raise HTTPException(status_code=400, detail="Agent already has a wallet")
    
    wallet = Wallet(
        id=str(uuid.uuid4()),
        agent_id=agent_id,
        address=wallet_data.address,
        wallet_type=wallet_data.wallet_type,
        ydm_balance=0.0,
        eth_balance=0.0
    )
    
    db.add(wallet)
    db.commit()
    db.refresh(wallet)
    
    return {
        "status": "success",
        "wallet_id": wallet.id,
        "address": wallet.address,
        "type": wallet.wallet_type,
        "ydm_balance": wallet.ydm_balance
    }

@router.get("/{agent_id}")
@limiter.limit("10/minute")
async def get_wallet(
    request: Request,
    agent_id: str,
    db: Session = Depends(get_db)
):
    wallet = db.query(Wallet).filter(Wallet.agent_id == agent_id).first()
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    
    return {
        "status": "success",
        "wallet": {
            "id": wallet.id,
            "address": wallet.address,
            "type": wallet.wallet_type,
            "ydm_balance": wallet.ydm_balance,
            "eth_balance": wallet.eth_balance
        }
    }
