from sqlalchemy import Column, String, Float, DateTime, Integer, Enum
from sqlalchemy.sql import func
import enum
from app.models.base import Base

class AgentType(str, enum.Enum):
    PUBLISHER = "publisher"
    ADVERTISER = "advertiser"
    ARBITRAGE = "arbitrage"

class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"

class Agent(Base):
    __tablename__ = "agents"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    type = Column(Enum(AgentType), nullable=False)
    status = Column(Enum(AgentStatus), default=AgentStatus.ACTIVE)
    
    # Performance & Trust
    performance_score = Column(Float, default=0.0)  # 0.0 - 1.0
    trust_level = Column(Integer, default=50)  # 0 - 100
    
    # Finanzen
    commission_earned_total = Column(Float, default=0.0)
    wallet_address = Column(String, nullable=True)
    
    # Für Advertiser: Bidding Budget
    daily_budget = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
