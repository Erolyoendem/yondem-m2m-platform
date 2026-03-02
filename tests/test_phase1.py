"""
Phase 1 – Foundation: Product, Shop, Deal model tests (migrated to pytest-asyncio).
"""
import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deal import Deal
from app.models.product import Product
from app.models.shop import Shop


async def test_create_product(db_session: AsyncSession):
    product = Product(name="Milch Bio", price=1.99, shop_id=1, currency="EUR")
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    assert product.id is not None
    assert product.name == "Milch Bio"
    assert product.currency == "EUR"


async def test_product_currency(db_session: AsyncSession):
    product = Product(name="Widget USD", price=9.99, shop_id=1, currency="USD")
    db_session.add(product)
    await db_session.commit()
    await db_session.refresh(product)
    assert product.currency == "USD"


async def test_create_shop(db_session: AsyncSession):
    shop = Shop(name="Amazon DE", commission_rate=0.08)
    db_session.add(shop)
    await db_session.commit()
    await db_session.refresh(shop)
    assert shop.id is not None
    assert shop.name == "Amazon DE"


async def test_shop_cashback(db_session: AsyncSession):
    shop = Shop(name="Zalando", commission_rate=0.10, cashback_rate=0.05)
    db_session.add(shop)
    await db_session.commit()
    await db_session.refresh(shop)
    assert shop.cashback_rate == pytest.approx(0.05)


async def test_create_deal(db_session: AsyncSession):
    deal = Deal(title="50% Rabatt", discount_value=50.0, discount_type="percent", shop_id=1)
    db_session.add(deal)
    await db_session.commit()
    await db_session.refresh(deal)
    assert deal.id is not None
    assert deal.title == "50% Rabatt"


async def test_deal_with_code(db_session: AsyncSession):
    deal = Deal(
        title="10 EUR Rabatt",
        discount_value=10.0,
        discount_type="fixed",
        code="SAVE10",
        shop_id=1,
    )
    db_session.add(deal)
    await db_session.commit()
    await db_session.refresh(deal)
    assert deal.code == "SAVE10"
