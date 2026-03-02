from sqlalchemy import Column, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
from app.models.base import Base

class IoTDevice(Base):
    __tablename__ = "iot_devices"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    device_type = Column(String, nullable=False)  # fridge, printer, sensor, etc.
    status = Column(String, default="active")  # active, inactive, error
    last_seen = Column(DateTime, default=func.now())
    api_key = Column(String, unique=True, nullable=False)
    # Automatisierung
    auto_order_enabled = Column(Boolean, default=False)
    budget_limit = Column(Float, default=0.0)  # 0 = unlimited
    preferred_shop_id = Column(String, ForeignKey("shops.id"), nullable=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
