from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
import logging
from app.services.contract_engine import check_all_contracts

logger = logging.getLogger("yondem")
scheduler = None

def init_scheduler():
    global scheduler
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        check_all_contracts,
        trigger=IntervalTrigger(seconds=60),
        id="check_contracts",
        name="Check Smart Contracts",
        replace_existing=True
    )
    scheduler.start()
    logger.info("Background scheduler started with contract checking every 60s")
    return scheduler

def shutdown_scheduler():
    if scheduler:
        scheduler.shutdown()
        logger.info("Background scheduler shutdown")
