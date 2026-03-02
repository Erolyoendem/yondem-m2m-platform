from app.models.base import Base, Column, Integer, String, Float, DateTime, Text, Boolean
from datetime import datetime

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    description = Column(Text)
    price = Column(Float, nullable=False)
    currency = Column(String(3), default='EUR')
    shop_id = Column(Integer, nullable=False)
    category = Column(String(100))
    image_url = Column(String(500))
    product_url = Column(String(500))
    affiliate_url = Column(String(500))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
