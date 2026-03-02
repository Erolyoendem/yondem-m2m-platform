from sqlalchemy import Column, String, Float, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
import enum
from app.models.base import Base

class WalletType(str, enum.Enum):
    ETHEREUM = "ethereum"
    POLYGON = "polygon"
    BITCOIN = "bitcoin"

class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(String, primary_key=True)
    agent_id = Column(String, ForeignKey("agents.id"), nullable=False, unique=True)
    
    # Wallet Details
    address = Column(String, nullable=False)
    wallet_type = Column(String, default=WalletType.POLYGON)
    
    # Balances
    ydm_balance = Column(Float, default=0.0)  # Yondem Token
    eth_balance = Column(Float, default=0.0)  # Native Token
    
    # Status
    is_active = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
