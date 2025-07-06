"""
Inventory schemas for API requests and responses.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class VehicleBase(BaseModel):
    """Base vehicle schema."""

    vin: str
    year: int
    make: str
    model: str
    trim: Optional[str] = None
    body_style: Optional[str] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    engine: Optional[str] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    drivetrain: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    condition: Optional[str] = None
    status: str = "available"
    description: Optional[str] = None
    features: Optional[str] = None
    images: Optional[str] = None


class VehicleCreate(VehicleBase):
    """Schema for creating a vehicle."""

    pass


class VehicleUpdate(BaseModel):
    """Schema for updating a vehicle."""

    vin: Optional[str] = None
    year: Optional[int] = None
    make: Optional[str] = None
    model: Optional[str] = None
    trim: Optional[str] = None
    body_style: Optional[str] = None
    color: Optional[str] = None
    mileage: Optional[int] = None
    engine: Optional[str] = None
    transmission: Optional[str] = None
    fuel_type: Optional[str] = None
    drivetrain: Optional[str] = None
    price: Optional[Decimal] = None
    cost: Optional[Decimal] = None
    condition: Optional[str] = None
    status: Optional[str] = None
    description: Optional[str] = None
    features: Optional[str] = None
    images: Optional[str] = None


class VehicleResponse(VehicleBase):
    """Schema for vehicle response."""

    id: int
    dealership_id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
