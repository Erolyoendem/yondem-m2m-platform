from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from app.models.base import Base

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(String, primary_key=True)
    
    # Beteiligte Parteien
    publisher_id = Column(String, ForeignKey("agents.id"), nullable=False)
    advertiser_id = Column(String, ForeignKey("agents.id"), nullable=False)
    product_id = Column(String, ForeignKey("products.id"), nullable=True)
    contract_id = Column(String, ForeignKey("smart_contracts.id"), nullable=True)
    
    # Transaktions-Details
    product_price = Column(Float, nullable=False)
    commission_amount = Column(Float, nullable=False)  # Provision für Publisher
    platform_fee = Column(Float, default=0.0)  # 20% für Platform
    
    # Status
    status = Column(String, default="completed")  # pending, completed, refunded
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
