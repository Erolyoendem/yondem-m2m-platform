from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime


class ProductResponse(BaseModel):
    """Product data model"""
    id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    price: float = Field(..., description="Product price")
    currency: str = Field(..., description="Currency code (EUR, USD, etc.)")
    shop_id: str = Field(..., description="ID of the shop selling this product")
    description: Optional[str] = Field(None, description="Product description")
    url: Optional[str] = Field(None, description="Product URL")

    class Config:
        from_attributes = True

class ShopResponse(BaseModel):
    """Shop data model"""
    id: str = Field(..., description="Unique shop identifier")
    name: str = Field(..., description="Shop name")
    cashback_percent: Optional[float] = Field(None, description="Cashback percentage")
    cashback_fixed: Optional[float] = Field(None, description="Fixed cashback amount")
    currency: str = Field(..., description="Shop currency")

    class Config:
        from_attributes = True


class DealResponse(BaseModel):
    """Deal/Discount data model"""
    id: str = Field(..., description="Unique deal identifier")
    title: str = Field(..., description="Deal title")
    description: Optional[str] = Field(None, description="Deal description")
    discount_percent: Optional[float] = Field(None, description="Discount percentage")
    discount_code: Optional[str] = Field(None, description="Discount coupon code")
    valid_until: Optional[str] = Field(None, description="Deal expiration date (ISO format)")
    shop_id: str = Field(..., description="ID of the shop offering this deal")

    class Config:
        from_attributes = True

class MCPResponse(BaseModel):
    """Standard MCP API response wrapper"""
    status: str = Field(..., description="Response status: success or error")
    data: Optional[Any] = Field(None, description="Response payload data")
    message: str = Field(..., description="Human-readable response message")


class SearchProductsResponse(MCPResponse):
    """Response for product search"""
    data: List[ProductResponse] = Field(default_factory=list, description="List of matching products")


class ProductDetailsResponse(MCPResponse):
    """Response for single product details"""
    data: Optional[ProductResponse] = Field(None, description="Product details")


class PriceComparisonResponse(MCPResponse):
    """Response for price comparison"""
    data: Dict[str, Any] = Field(default_factory=dict, description="Price comparison by shop")


class DealsResponse(MCPResponse):
    """Response for deals listing"""
    data: List[DealResponse] = Field(default_factory=list, description="List of deals")


class CashbackInfoResponse(MCPResponse):
    """Response for cashback information"""
    data: Optional[ShopResponse] = Field(None, description="Shop cashback details")
