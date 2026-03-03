from sqlalchemy import String, Integer, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func
from datetime import datetime
from app.models.base import Base


class WaitlistEntry(Base):
    __tablename__ = "waitlist"
    __table_args__ = (
        Index("ix_waitlist_email", "email", unique=True),
        Index("ix_waitlist_type", "type"),
        Index("ix_waitlist_created_at", "created_at"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    email: Mapped[str] = mapped_column(String(255), nullable=False)
    type: Mapped[str] = mapped_column(String(50), nullable=False)  # publisher | advertiser
    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
