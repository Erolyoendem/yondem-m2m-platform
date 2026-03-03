from sqlalchemy import String, Float, Integer, Enum as SAEnum, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from typing import Optional
import enum
from app.models.base import Base


class AgentType(str, enum.Enum):
    PUBLISHER = "publisher"
    ADVERTISER = "advertiser"
    ARBITRAGE = "arbitrage"


class AgentStatus(str, enum.Enum):
    ACTIVE = "active"
    INACTIVE = "inactive"
    SUSPENDED = "suspended"


class Agent(Base):
    __tablename__ = "agents"
    __table_args__ = (
        Index("ix_agents_type", "type"),
        Index("ix_agents_status", "status"),
        Index("ix_agents_created_at", "created_at"),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    type: Mapped[AgentType] = mapped_column(
        SAEnum(AgentType, values_callable=lambda obj: [e.value for e in obj]), nullable=False
    )
    status: Mapped[AgentStatus] = mapped_column(
        SAEnum(AgentStatus, values_callable=lambda obj: [e.value for e in obj]),
        default=AgentStatus.ACTIVE
    )
    performance_score: Mapped[float] = mapped_column(Float, default=0.0)
    trust_level: Mapped[int] = mapped_column(Integer, default=50)
    commission_earned_total: Mapped[float] = mapped_column(Float, default=0.0)
    wallet_address: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    daily_budget: Mapped[float] = mapped_column(Float, default=0.0)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
