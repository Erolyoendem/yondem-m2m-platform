from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from pydantic import BaseModel
from typing import Optional
import os

from app.database.session import get_db
from app.models.waitlist import WaitlistEntry
from app.core.rate_limiter import limiter

router = APIRouter(prefix="/waitlist", tags=["Waitlist"])


class WaitlistCreate(BaseModel):
    name: str
    email: str
    type: str  # publisher | advertiser


@router.post("/")
@limiter.limit("5/minute")
async def join_waitlist(
    request: Request,
    data: WaitlistCreate,
    db: AsyncSession = Depends(get_db),
):
    if data.type not in ("publisher", "advertiser"):
        raise HTTPException(status_code=400, detail="type must be 'publisher' or 'advertiser'")

    result = await db.execute(select(WaitlistEntry).where(WaitlistEntry.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(status_code=400, detail="Email already on the waitlist")

    entry = WaitlistEntry(name=data.name, email=data.email, type=data.type)
    db.add(entry)
    await db.commit()
    await db.refresh(entry)

    return {
        "status": "success",
        "message": f"Welcome to the waitlist, {data.name}! We'll be in touch.",
        "id": entry.id,
        "type": entry.type,
    }


@router.get("/")
@limiter.limit("10/minute")
async def list_waitlist(
    request: Request,
    x_api_key: Optional[str] = Header(None),
    db: AsyncSession = Depends(get_db),
):
    api_key = os.getenv("API_KEY", "dev-api-key")
    if x_api_key != api_key:
        raise HTTPException(status_code=403, detail="Invalid or missing API key")

    result = await db.execute(
        select(WaitlistEntry).order_by(WaitlistEntry.created_at.desc())
    )
    entries = result.scalars().all()

    return {
        "status": "success",
        "count": len(entries),
        "entries": [
            {
                "id": e.id,
                "name": e.name,
                "email": e.email,
                "type": e.type,
                "created_at": str(e.created_at),
            }
            for e in entries
        ],
    }
