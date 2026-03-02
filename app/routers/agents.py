from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from pydantic import BaseModel
import uuid

from app.database.session import get_db
from app.models.agent import Agent, AgentType, AgentStatus
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/agents", tags=["Agent System"])

class AgentRegister(BaseModel):
    name: str
    type: str  # publisher, advertiser, arbitrage

@router.post("/register")
@limiter.limit("10/minute")
async def register_agent(
    request: Request,
    data: AgentRegister,
    db: Session = Depends(get_db)
):
    """Register a new Agent (Publisher, Advertiser, or Arbitrage)
    
    - **name**: Agent name
    - **type**: publisher | advertiser | arbitrage
    - Returns agent_id and type
    """
    agent_id = str(uuid.uuid4())
    
    try:
        agent_type = AgentType(data.type.lower())
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid agent type. Use: publisher, advertiser, or arbitrage")
    
    agent = Agent(
        id=agent_id,
        name=data.name,
        type=agent_type
    )
    db.add(agent)
    db.commit()
    db.refresh(agent)
    
    return {
        "status": "success",
        "agent_id": agent_id,
        "type": agent.type.value,
        "trust_level": agent.trust_level,
        "message": f"{agent_type.value} agent registered successfully"
    }

@router.get("/")
@limiter.limit("30/minute")
async def list_agents(
    request: Request,
    db: Session = Depends(get_db)
):
    """List all registered agents
    """
    agents = db.query(Agent).all()
    return {
        "status": "success",
        "count": len(agents),
        "agents": [{
            "id": a.id,
            "name": a.name,
            "type": a.type.value,
            "status": a.status.value,
            "trust_level": a.trust_level,
            "commission_earned": a.commission_earned_total
        } for a in agents]
    }

@router.get("/{agent_id}")
@limiter.limit("60/minute")
async def get_agent(
    request: Request,
    agent_id: str,
    db: Session = Depends(get_db)
):
    """Get details of a specific agent
    """
    agent = db.query(Agent).filter(Agent.id == agent_id).first()
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    return {
        "status": "success",
        "agent": {
            "id": agent.id,
            "name": agent.name,
            "type": agent.type.value,
            "status": agent.status.value,
            "trust_level": agent.trust_level,
            "performance_score": agent.performance_score,
            "commission_earned": agent.commission_earned_total,
            "wallet": agent.wallet_address,
            "daily_budget": agent.daily_budget
        }
    }
