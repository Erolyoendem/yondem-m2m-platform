from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
import uuid

from app.database.session import get_db
from app.models.smart_contract import SmartContract
from app.models.agent import Agent, AgentType
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/contracts", tags=["Smart Contracts"])


class ContractRules(BaseModel):
    product: str
    condition: str
    max_price: float
    preferred_shop_id: Optional[str] = None


@router.post("/{agent_id}/create")
@limiter.limit("5/minute")
async def create_contract(
    request: Request,
    agent_id: str,
    rules: ContractRules,
    monthly_budget: float = 100.0,
    db: AsyncSession = Depends(get_db),
):
    """Create a Smart Contract for a Publisher Agent."""
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    if agent.type != AgentType.PUBLISHER:
        raise HTTPException(
            status_code=403, detail="Only Publisher agents can create contracts"
        )

    contract_id = str(uuid.uuid4())
    contract = SmartContract(
        id=contract_id,
        agent_id=agent_id,
        rules=rules.model_dump(),
        monthly_budget=monthly_budget,
    )
    db.add(contract)
    await db.commit()
    await db.refresh(contract)

    return {
        "status": "success",
        "contract_id": contract_id,
        "agent_id": agent_id,
        "rules": rules.model_dump(),
        "monthly_budget": monthly_budget,
        "message": "Smart contract created successfully",
    }


@router.get("/{agent_id}/list")
@limiter.limit("30/minute")
async def list_contracts(
    request: Request,
    agent_id: str,
    db: AsyncSession = Depends(get_db),
):
    """List all Smart Contracts for a given Agent."""
    result_agent = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result_agent.scalar_one_or_none()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")

    result = await db.execute(
        select(SmartContract).where(SmartContract.agent_id == agent_id)
    )
    contracts = result.scalars().all()

    return {
        "status": "success",
        "agent_id": agent_id,
        "count": len(contracts),
        "contracts": [
            {
                "id": c.id,
                "rules": c.rules,
                "is_active": bool(c.is_active),
                "monthly_budget": c.monthly_budget,
                "spent_this_month": c.spent_this_month,
                "execution_count": c.execution_count,
                "success_count": c.success_count,
                "created_at": c.created_at.isoformat() if c.created_at else None,
            }
            for c in contracts
        ],
    }
