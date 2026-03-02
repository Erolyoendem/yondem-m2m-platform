from sqlalchemy import String, Float, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
from app.models.base import Base


class Transaction(Base):
    __tablename__ = "transactions"
    __table_args__ = (
        Index("ix_transactions_publisher_id", "publisher_id"),
        Index("ix_transactions_advertiser_id", "advertiser_id"),
        Index("ix_transactions_created_at", "created_at"),
        Index("ix_transactions_status", "status"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    publisher_id: Mapped[str] = mapped_column(String, ForeignKey("agents.id"), nullable=False)
    advertiser_id: Mapped[str] = mapped_column(String, ForeignKey("agents.id"), nullable=False)
    product_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("products.id"), nullable=True
    )
    contract_id: Mapped[Optional[str]] = mapped_column(
        String, ForeignKey("smart_contracts.id"), nullable=True
    )
    product_price: Mapped[float] = mapped_column(Float, nullable=False)
    commission_amount: Mapped[float] = mapped_column(Float, nullable=False)
    platform_fee: Mapped[float] = mapped_column(Float, default=0.0)
    status: Mapped[str] = mapped_column(String, default="completed")
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
