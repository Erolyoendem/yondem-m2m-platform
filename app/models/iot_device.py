from sqlalchemy import String, Float, Boolean, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from app.models.base import Base


class IoTDevice(Base):
    __tablename__ = "iot_devices"
    __table_args__ = (Index("ix_iot_devices_status", "status"),)

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    device_type: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[str] = mapped_column(String, default="active")
    last_seen: Mapped[datetime] = mapped_column(server_default=func.now())
    api_key: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    auto_order_enabled: Mapped[bool] = mapped_column(Boolean, default=False)
    budget_limit: Mapped[float] = mapped_column(Float, default=0.0)
    preferred_shop_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("shops.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
