from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from app.models.base import Base

class Bid(Base):
    __tablename__ = "bids"

    id = Column(String, primary_key=True)
    
    # Wer bietet
    advertiser_id = Column(String, ForeignKey("agents.id"), nullable=False)
    
    # Für welches Produkt/Kategorie
    product_category = Column(String, nullable=False)  # z.B. "dairy", "electronics"
    target_product = Column(String, nullable=True)  # Spezifisches Produkt
    
    # Bidding Details
    commission_rate = Column(Float, default=0.10)  # 10% Provision
    max_cpc = Column(Float, default=0.50)  # Max Cost Per Click
    daily_budget = Column(Float, default=100.0)
    
    # Status
    is_active = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
