from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from app.services.contract_engine import check_all_contracts

logger = logging.getLogger("yondem")
scheduler = None


def refresh_affiliate_offers():
    """
    Aktualisiert Affiliate-Angebote aus Awin + Digistore24 in der DB.
    Läuft alle 6 Stunden via BackgroundScheduler.
    """
    try:
        from app.services.awin_client import get_best_offers as awin_offers
        from app.services.digistore_client import get_top_products as ds_products
        from app.models.affiliate_offer import AffiliateOffer
        from app.database.session import SyncSessionLocal

        offers = []
        try:
            offers.extend(awin_offers(min_commission=5.0, max_results=20))
        except Exception as exc:
            logger.warning("Awin refresh failed: %s", exc)
        try:
            offers.extend(ds_products(min_commission=0.0, max_results=20))
        except Exception as exc:
            logger.warning("Digistore24 refresh failed: %s", exc)

        if not offers:
            logger.info("Affiliate refresh: no offers retrieved")
            return

        with SyncSessionLocal() as db:
            # Bestehende Offers löschen und neu eintragen (full refresh)
            db.query(AffiliateOffer).delete()
            for o in offers:
                db.add(AffiliateOffer(
                    network=o.get("network", "unknown"),
                    advertiser_name=o.get("advertiser_name", ""),
                    product_name=o.get("product_name", ""),
                    commission_rate=float(o.get("commission_rate", 0)),
                    conversion_rate=float(o.get("conversion_rate", 0)),
                    url=o.get("url", ""),
                ))
            db.commit()
            logger.info("Affiliate refresh: %d offers saved to DB", len(offers))

    except Exception as exc:
        logger.error("refresh_affiliate_offers error: %s", exc, exc_info=True)


def init_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()

    # Job 1: Smart Contracts prüfen – alle 60 Sekunden
    scheduler.add_job(
        check_all_contracts,
        trigger=IntervalTrigger(seconds=60),
        id="check_contracts",
        name="Check Smart Contracts",
        replace_existing=True,
    )

    # Job 2: Affiliate Angebote aktualisieren – alle 6 Stunden
    scheduler.add_job(
        refresh_affiliate_offers,
        trigger=IntervalTrigger(hours=6),
        id="refresh_affiliate_offers",
        name="Refresh Affiliate Offers (Awin + Digistore24)",
        replace_existing=True,
    )

    scheduler.start()
    logger.info(
        "Background scheduler started: contracts every 60s, affiliate offers every 6h"
    )
    return scheduler


def shutdown_scheduler():
    if scheduler:
        scheduler.shutdown()
        logger.info("Background scheduler shutdown")
