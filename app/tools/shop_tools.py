from typing import Dict, List, Optional, Any

from sqlalchemy.orm import Session
from sqlalchemy import func, or_

from app.services.i18n import i18n_service
from app.database.session import get_db
from app.models.product import Product
from app.models.shop import Shop
from app.models.deal import Deal


class ShopTools:
    """MCP Tools for shop and product operations with real DB queries"""

    def __init__(self, db: Session = None):
        self.db = db or next(get_db())

    async def search_products(self, query: str, lang: str = "de") -> Dict[str, Any]:
        """Search for products across all shops"""
        search_filter = or_(
            Product.name.ilike(f"%{query}%"),
            Product.description.ilike(f"%{query}%")
        )
        products = self.db.query(Product).filter(search_filter).all()
        data = [{"id": p.id, "name": p.name, "price": p.price, "currency": p.currency, "shop_id": p.shop_id} for p in products]
        return {
            "status": "success",
            "data": data,
            "message": i18n_service.translate("products_found", lang, count=len(data))
        }

    async def get_product_details(self, product_id: str, lang: str = "de") -> Dict[str, Any]:
        """Get detailed information about a specific product"""
        product = self.db.query(Product).filter(Product.id == product_id).first()
        if not product:
            return {
                "status": "error",
                "message": i18n_service.translate("product_not_found", lang)
            }
        return {
            "status": "success",
            "data": {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "currency": product.currency,
                "url": product.url,
                "shop_id": product.shop_id
            },
            "message": i18n_service.translate("product_details_loaded", lang)
        }

    async def compare_prices(self, product_name: str, lang: str = "de") -> Dict[str, Any]:
        """Compare prices across different shops"""
        products = self.db.query(Product, Shop).join(Shop, Product.shop_id == Shop.id).filter(
            Product.name.ilike(f"%{product_name}%")
        ).all()
        prices = {}
        for product, shop in products:
            prices[shop.name] = {
                "price": product.price,
                "currency": product.currency,
                "url": product.url,
                "cashback_percent": shop.cashback_percent
            }
        return {
            "status": "success",
            "data": prices,
            "message": i18n_service.translate("price_comparison_ready", lang)
        }

    async def get_deals(self, category: Optional[str] = None, lang: str = "de") -> Dict[str, Any]:
        """Get current deals and offers"""
        query = self.db.query(Deal)
        if category:
            query = query.filter(Deal.category == category)
        deals = query.all()
        data = [{
            "id": d.id,
            "title": d.title,
            "description": d.description,
            "discount_percent": d.discount_percent,
            "discount_code": d.discount_code,
            "valid_until": d.valid_until.isoformat() if d.valid_until else None,
            "shop_id": d.shop_id
        } for d in deals]
        return {
            "status": "success",
            "data": data,
            "message": i18n_service.translate("deals_loaded", lang, count=len(data))
        }

    async def get_cashback_info(self, shop_id: str, lang: str = "de") -> Dict[str, Any]:
        """Get cashback information for a specific shop"""
        shop = self.db.query(Shop).filter(Shop.id == shop_id).first()
        if not shop:
            return {
                "status": "error",
                "message": i18n_service.translate("shop_not_found", lang)
            }
        return {
            "status": "success",
            "data": {
                "shop_id": shop.id,
                "shop_name": shop.name,
                "cashback_percent": shop.cashback_percent,
                "cashback_fixed": shop.cashback_fixed,
                "currency": shop.currency
            },
            "message": i18n_service.translate("cashback_info_loaded", lang)
        }
