from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import Dict, Any
import uuid

from app.database.session import get_db
from app.models.smart_contract import SmartContract
from app.models.agent import Agent, AgentType
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/contracts", tags=["Smart Contracts"])

class ContractRules(BaseModel):
    product: str
    condition: str  # e.g., "stock < 2"
    max_price: float
    preferred_shop_id: str = None

@router.post("/{agent_id}/create")
@limiter.limit("5/minute")
async def create_contract(
    request: Request,
    agent_id: str,
    rules: ContractRules,
    monthly_budget: float = 100.0,
    db: Session = Depends(get_db)
):
    """Create a Smart Contract for an Agent (Publisher only)
    
    - **agent_id**: UUID of the Publisher Agent
    - **rules**: {product, condition, max_price, preferred_shop_id}
    - **monthly_budget**: Maximum spend per month
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.type != AgentType.PUBLISHER:
        raise HTTPException(status_code=403, detail="Only Publisher agents can create contracts")
    
    contract_id = str(uuid.uuid4())
    contract = SmartContract(
        id=contract_id,
        agent_id=agent_id,
        rules=rules.dict(),
        monthly_budget=monthly_budget
    )
    db.add(contract)
    db.commit()
    db.refresh(contract)
    
    return {
        "status": "success",
        "contract_id": contract_id,
        "agent_id": agent_id,
        "rules": rules.dict(),
        "monthly_budget": monthly_budget,
        "message": "Smart contract created successfully"
    }
