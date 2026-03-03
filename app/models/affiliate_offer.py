from sqlalchemy import String, Integer, Float, Index, DateTime
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from app.models.base import Base


class AffiliateOffer(Base):
    __tablename__ = "affiliate_offers"
    __table_args__ = (
        Index("ix_affiliate_offers_network", "network"),
        Index("ix_affiliate_offers_commission", "commission_rate"),
        Index("ix_affiliate_offers_last_updated", "last_updated"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    network: Mapped[str] = mapped_column(String(50), nullable=False)          # awin | digistore24
    advertiser_name: Mapped[str] = mapped_column(String(255), nullable=False)
    product_name: Mapped[str] = mapped_column(String(500), nullable=False)
    commission_rate: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    conversion_rate: Mapped[float] = mapped_column(Float, nullable=True, default=0.0)
    url: Mapped[str] = mapped_column(String(1000), nullable=True)
    last_updated: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )
