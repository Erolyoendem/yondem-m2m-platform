from sqlalchemy import Column, String, Float, DateTime, Integer, ForeignKey, JSON
from sqlalchemy.sql import func
from app.models.base import Base

class SmartContract(Base):
    __tablename__ = "smart_contracts"

    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False)
    
    # Regel-Konfiguration (JSON)
    rules = Column(JSON, nullable=False)  # {product: "milk", condition: "stock < 2", max_price: 2.5}
    
    # Ausführungs-Tracking
    is_active = Column(Integer, default=1)  # 1 = active, 0 = inactive
    execution_count = Column(Integer, default=0)
    success_count = Column(Integer, default=0)
    last_executed = Column(DateTime, nullable=True)
    
    # Budget & Limits
    monthly_budget = Column(Float, default=100.0)
    spent_this_month = Column(Float, default=0.0)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
