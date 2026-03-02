from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from uuid import UUID

class Agent(BaseModel):
    id: UUID
    name: str
    email: str
    agent_type: str
    created_at: datetime

    class Config:
        from_attributes = True

class ShopProgram(BaseModel):
    id: UUID
    agent_id: UUID
    shop_name: str
    commission_rate: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class AgentDeal(BaseModel):
    id: UUID
    shop_program_id: UUID
    publisher_agent_id: UUID
    commission_rate: float
    status: str
    created_at: datetime

    class Config:
        from_attributes = True

class DealCreate(BaseModel):
    shop_program_id: UUID
    publisher_agent_id: UUID
    commission_rate: float = Field(..., ge=0, le=100)
