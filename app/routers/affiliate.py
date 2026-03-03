"""
Affiliate Router
-----------------
GET  /affiliate/offers             – beste Angebote aus Awin + Digistore24
GET  /affiliate/match/{publisher_id} – bestes Angebot für Publisher
POST /affiliate/track              – Conversion Tracking
"""
from __future__ import annotations

import logging
import uuid
from datetime import datetime, timezone
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.rate_limiter import limiter
from app.database.session import get_db
from app.models.affiliate_offer import AffiliateOffer
from app.services.awin_client import get_best_offers as awin_offers
from app.services.digistore_client import get_top_products as ds_products

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/affiliate", tags=["Affiliate"])


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

class ConversionTrack(BaseModel):
    publisher_id: str
    offer_id: int
    amount: Optional[float] = None
    currency: str = "EUR"
    meta: Optional[dict] = None


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@router.get("/offers")
@limiter.limit("30/minute")
async def get_offers(
    request: Request,
    network: Optional[str] = None,
    min_commission: float = 0.0,
    limit: int = 20,
    db: AsyncSession = Depends(get_db),
):
    """
    Gibt die besten Affiliate-Angebote aus der DB zurück (gecacht).
    Falls DB leer → live von Awin + Digistore24 laden.
    """
    stmt = select(AffiliateOffer).order_by(
        AffiliateOffer.commission_rate.desc()
    ).limit(limit)

    if network:
        stmt = stmt.where(AffiliateOffer.network == network)
    if min_commission > 0:
        stmt = stmt.where(AffiliateOffer.commission_rate >= min_commission)

    result = await db.execute(stmt)
    offers = result.scalars().all()

    if offers:
        return {
            "status": "ok",
            "source": "cache",
            "count": len(offers),
            "offers": [_offer_dict(o) for o in offers],
        }

    # DB leer → live laden und zusammenführen
    live = _fetch_live_offers(min_commission=min_commission, limit=limit)
    return {
        "status": "ok",
        "source": "live",
        "count": len(live),
        "offers": live,
    }


@router.get("/match/{publisher_id}")
@limiter.limit("20/minute")
async def match_offer(
    request: Request,
    publisher_id: str,
    db: AsyncSession = Depends(get_db),
):
    """
    Gibt das beste Affiliate-Angebot für einen Publisher zurück.
    Wählt nach höchster commission_rate × conversion_rate (Erwartungswert).
    """
    result = await db.execute(
        select(AffiliateOffer).order_by(AffiliateOffer.commission_rate.desc()).limit(50)
    )
    offers = result.scalars().all()

    if not offers:
        live = _fetch_live_offers(limit=50)
        if not live:
            raise HTTPException(status_code=404, detail="No affiliate offers available")
        best = max(live, key=lambda x: x["commission_rate"] * (x.get("conversion_rate") or 1))
        return {"status": "ok", "publisher_id": publisher_id, "best_offer": best}

    # Erwartungswert = commission_rate × conversion_rate
    best_offer = max(
        offers,
        key=lambda o: o.commission_rate * (o.conversion_rate or 1.0),
    )
    return {
        "status": "ok",
        "publisher_id": publisher_id,
        "best_offer": _offer_dict(best_offer),
    }


@router.post("/track")
@limiter.limit("60/minute")
async def track_conversion(
    request: Request,
    data: ConversionTrack,
    db: AsyncSession = Depends(get_db),
):
    """
    Conversion Tracking – speichert eine Affiliate-Conversion.
    Verknüpft Publisher mit Angebot und Betrag.
    """
    result = await db.execute(
        select(AffiliateOffer).where(AffiliateOffer.id == data.offer_id)
    )
    offer = result.scalar_one_or_none()
    if not offer:
        raise HTTPException(status_code=404, detail=f"Offer {data.offer_id} not found")

    conversion_id = str(uuid.uuid4())
    logger.info(
        "Conversion tracked: id=%s publisher=%s offer=%s amount=%s %s",
        conversion_id,
        data.publisher_id,
        data.offer_id,
        data.amount,
        data.currency,
    )

    commission = round((data.amount or 0) * offer.commission_rate / 100, 4)

    return {
        "status": "ok",
        "conversion_id": conversion_id,
        "publisher_id": data.publisher_id,
        "offer_id": data.offer_id,
        "amount": data.amount,
        "currency": data.currency,
        "commission_earned": commission,
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _offer_dict(o: AffiliateOffer) -> dict:
    return {
        "id": o.id,
        "network": o.network,
        "advertiser_name": o.advertiser_name,
        "product_name": o.product_name,
        "commission_rate": o.commission_rate,
        "conversion_rate": o.conversion_rate,
        "url": o.url,
        "last_updated": str(o.last_updated) if o.last_updated else None,
    }


def _fetch_live_offers(min_commission: float = 0.0, limit: int = 20) -> list[dict]:
    """Kombiniert live Awin + Digistore24 Offers."""
    combined = []
    try:
        combined.extend(awin_offers(min_commission=min_commission, max_results=limit // 2))
    except Exception as exc:
        logger.warning("Awin live fetch failed: %s", exc)
    try:
        combined.extend(ds_products(min_commission=min_commission, max_results=limit // 2))
    except Exception as exc:
        logger.warning("Digistore24 live fetch failed: %s", exc)

    combined.sort(key=lambda x: x.get("commission_rate", 0), reverse=True)
    return combined[:limit]
