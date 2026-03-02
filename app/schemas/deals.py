from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class AgentDeal(BaseModel):
    id: str
    shop_program_id: str
    publisher_agent_id: str
    commission_rate: float
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class DealCreate(BaseModel):
    shop_program_id: str
    publisher_agent_id: str
    commission_rate: float
