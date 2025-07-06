"""
Sale schemas for API requests and responses.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class SaleBase(BaseModel):
    """Base sale schema."""

    vehicle_id: int
    customer_id: int
    salesperson_id: int
    sale_price: Decimal
    down_payment: Optional[Decimal] = None
    trade_in_value: Optional[Decimal] = None
    trade_in_vehicle: Optional[str] = None
    financing_amount: Optional[Decimal] = None
    interest_rate: Optional[Decimal] = None
    loan_term: Optional[int] = None
    monthly_payment: Optional[Decimal] = None
    sale_type: str = "retail"
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class SaleCreate(SaleBase):
    """Schema for creating a sale."""

    pass


class SaleUpdate(BaseModel):
    """Schema for updating a sale."""

    vehicle_id: Optional[int] = None
    customer_id: Optional[int] = None
    salesperson_id: Optional[int] = None
    sale_price: Optional[Decimal] = None
    down_payment: Optional[Decimal] = None
    trade_in_value: Optional[Decimal] = None
    trade_in_vehicle: Optional[str] = None
    financing_amount: Optional[Decimal] = None
    interest_rate: Optional[Decimal] = None
    loan_term: Optional[int] = None
    monthly_payment: Optional[Decimal] = None
    sale_type: Optional[str] = None
    payment_method: Optional[str] = None
    notes: Optional[str] = None


class SaleResponse(SaleBase):
    """Schema for sale response."""

    id: int
    dealership_id: int
    sale_date: datetime
    status: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
