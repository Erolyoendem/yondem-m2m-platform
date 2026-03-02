from typing import Any, Dict, Optional

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.deal import Deal
from app.models.product import Product
from app.models.shop import Shop
from app.services.i18n import i18n_service


class ShopTools:
    """MCP Tools – async SQLAlchemy queries."""

    def __init__(self, db: AsyncSession):
        self.db = db

    async def search_products(self, query: str, lang: str = "de") -> Dict[str, Any]:
        stmt = select(Product).where(
            or_(Product.name.ilike(f"%{query}%"), Product.description.ilike(f"%{query}%"))
        )
        result = await self.db.execute(stmt)
        products = result.scalars().all()
        data = [
            {"id": p.id, "name": p.name, "price": p.price, "currency": p.currency, "shop_id": p.shop_id}
            for p in products
        ]
        return {
            "status": "success",
            "data": data,
            "message": i18n_service.translate("products_found", lang, count=len(data)),
        }

    async def get_product_details(self, product_id: str, lang: str = "de") -> Dict[str, Any]:
        result = await self.db.execute(select(Product).where(Product.id == product_id))
        product = result.scalar_one_or_none()
        if not product:
            return {"status": "error", "message": i18n_service.translate("product_not_found", lang)}
        return {
            "status": "success",
            "data": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "currency": product.currency,
                "shop_id": product.shop_id,
            },
            "message": i18n_service.translate("product_details_loaded", lang),
        }

    async def compare_prices(self, product_name: str, lang: str = "de") -> Dict[str, Any]:
        stmt = (
            select(Product, Shop)
            .join(Shop, Product.shop_id == Shop.id)
            .where(Product.name.ilike(f"%{product_name}%"))
        )
        result = await self.db.execute(stmt)
        rows = result.all()
        prices = {
            shop.name: {"price": product.price, "currency": product.currency}
            for product, shop in rows
        }
        return {
            "status": "success",
            "data": prices,
            "message": i18n_service.translate("price_comparison_ready", lang),
        }

    async def get_deals(self, category: Optional[str] = None, lang: str = "de") -> Dict[str, Any]:
        stmt = select(Deal)
        if category:
            stmt = stmt.where(Deal.category == category)
        result = await self.db.execute(stmt)
        deals = result.scalars().all()
        data = [
            {
                "id": d.id,
                "title": d.title,
                "discount_value": d.discount_value,
                "valid_until": d.valid_until.isoformat() if d.valid_until else None,
                "shop_id": d.shop_id,
            }
            for d in deals
        ]
        return {
            "status": "success",
            "data": data,
            "message": i18n_service.translate("deals_loaded", lang, count=len(data)),
        }

    async def get_cashback_info(self, shop_id: str, lang: str = "de") -> Dict[str, Any]:
        result = await self.db.execute(select(Shop).where(Shop.id == shop_id))
        shop = result.scalar_one_or_none()
        if not shop:
            return {"status": "error", "message": i18n_service.translate("shop_not_found", lang)}
        return {
            "status": "success",
            "data": {
                "shop_id": shop.id,
                "shop_name": shop.name,
                "cashback_rate": shop.cashback_rate,
                "commission_rate": shop.commission_rate,
            },
            "message": i18n_service.translate("cashback_info_loaded", lang),
        }
