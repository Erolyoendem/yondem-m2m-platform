import logging
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.base import Base
from app.config import settings

logger = logging.getLogger("yondem")

# ── Async engine (API routes) ──────────────────────────────────────────────
_async_url = settings.DATABASE_URL
_async_connect_args: dict = {}
if "sqlite" in _async_url:
    _async_connect_args = {"check_same_thread": False}
elif "asyncpg" in _async_url:
    # PgBouncer (Supabase pooler) requires prepared statements disabled
    _async_connect_args = {"statement_cache_size": 0}

async_engine = create_async_engine(
    _async_url,
    echo=False,
    connect_args=_async_connect_args,
)

AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session


async def init_db() -> None:
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database initialized (async)")


# ── Sync engine (background scheduler only) ────────────────────────────────
_sync_url = (
    _async_url
    .replace("+asyncpg", "")
    .replace("+aiosqlite", "")
)
_sync_connect_args: dict = {"check_same_thread": False} if "sqlite" in _sync_url else {}

sync_engine = create_engine(_sync_url, connect_args=_sync_connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=sync_engine)


def init_db_sync() -> None:
    Base.metadata.create_all(bind=sync_engine)
    logger.info("Database initialized (sync)")
