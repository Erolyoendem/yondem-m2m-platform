from sqlalchemy import String, Float, Integer, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from app.models.base import Base


class Bid(Base):
    __tablename__ = "bids"
    __table_args__ = (
        Index("ix_bids_advertiser_id", "advertiser_id"),
        Index("ix_bids_product_category", "product_category"),
        Index("ix_bids_is_active", "is_active"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    advertiser_id: Mapped[str] = mapped_column(String, ForeignKey("agents.id"), nullable=False)
    product_category: Mapped[str] = mapped_column(String, nullable=False)
    target_product: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    commission_rate: Mapped[float] = mapped_column(Float, default=0.10)
    max_cpc: Mapped[float] = mapped_column(Float, default=0.50)
    daily_budget: Mapped[float] = mapped_column(Float, default=100.0)
    is_active: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
