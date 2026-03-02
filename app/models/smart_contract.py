from sqlalchemy import String, Float, Integer, ForeignKey, JSON, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional, Any
from app.models.base import Base


class SmartContract(Base):
    __tablename__ = "smart_contracts"
    __table_args__ = (
        Index("ix_smart_contracts_agent_id", "agent_id"),
        Index("ix_smart_contracts_is_active", "is_active"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    agent_id: Mapped[str] = mapped_column(String, ForeignKey("agents.id"), nullable=False)
    rules: Mapped[Any] = mapped_column(JSON, nullable=False)
    is_active: Mapped[int] = mapped_column(Integer, default=1)
    execution_count: Mapped[int] = mapped_column(Integer, default=0)
    success_count: Mapped[int] = mapped_column(Integer, default=0)
    last_executed: Mapped[Optional[datetime]] = mapped_column(nullable=True)
    monthly_budget: Mapped[float] = mapped_column(Float, default=100.0)
    spent_this_month: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
