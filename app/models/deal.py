from app.models.base import Base, Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

class Deal(Base):
    __tablename__ = 'deals'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000))
    discount_value = Column(Float)
    discount_type = Column(String(20))
    code = Column(String(50))
    shop_id = Column(Integer, nullable=False)
    product_id = Column(Integer)
    category = Column(String(100))
    valid_from = Column(DateTime)
    valid_until = Column(DateTime)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
