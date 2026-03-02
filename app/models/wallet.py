from sqlalchemy import String, Float, Integer, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
import enum
from app.models.base import Base


class WalletType(str, enum.Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BITCOIN = "bitcoin"


class Wallet(Base):
    __tablename__ = "wallets"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    agent_id: Mapped[str] = mapped_column(
        String, ForeignKey("agents.id"), nullable=False, unique=True
    )
    address: Mapped[str] = mapped_column(String, nullable=False)
    wallet_type: Mapped[str] = mapped_column(String, default=WalletType.POLYGON)
    ydm_balance: Mapped[float] = mapped_column(Float, default=0.0)
    eth_balance: Mapped[float] = mapped_column(Float, default=0.0)
    is_active: Mapped[int] = mapped_column(Integer, default=1)
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(server_default=func.now(), onupdate=func.now())
