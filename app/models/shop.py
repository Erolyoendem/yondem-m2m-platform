from app.models.base import Base, Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

class Shop(Base):
    __tablename__ = 'shops'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    logo_url = Column(String(500))
    website_url = Column(String(500))
    affiliate_network = Column(String(100))
    commission_rate = Column(Float)
    cashback_rate = Column(Float)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
