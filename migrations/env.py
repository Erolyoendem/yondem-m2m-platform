"""Alembic env.py – async-compatible with SQLAlchemy 2.0."""
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

# ── Load app config so DATABASE_URL comes from .env ────────────────────────
from app.config import settings

# ── Load models so autogenerate detects all tables ─────────────────────────
from app.models.base import Base
from app.models import (  # noqa: F401
    Product, Shop, Deal, IoTDevice,
    Agent, SmartContract, Transaction, Bid, Wallet,
)

config = context.config

if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Override URL from .env so alembic.ini is ignored for the connection
config.set_main_option("sqlalchemy.url", settings.DATABASE_URL)

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    connect_args = {}
    if "asyncpg" in settings.DATABASE_URL:
        connect_args = {"statement_cache_size": 0}
    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
        connect_args=connect_args,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
