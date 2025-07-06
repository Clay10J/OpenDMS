"""
Dealership schemas for API requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class DealershipBase(BaseModel):
    """Base dealership schema."""

    name: str
    legal_name: Optional[str] = None
    dealer_number: str
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    address_line_1: str
    address_line_2: Optional[str] = None
    city: str
    state: str
    zip_code: str
    country: str = "USA"
    tax_id: Optional[str] = None
    business_license: Optional[str] = None
    dealer_license: Optional[str] = None
    operating_hours: Optional[str] = None


class DealershipCreate(DealershipBase):
    """Schema for creating a dealership."""

    pass


class DealershipUpdate(BaseModel):
    """Schema for updating a dealership."""

    name: Optional[str] = None
    legal_name: Optional[str] = None
    dealer_number: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    website: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    tax_id: Optional[str] = None
    business_license: Optional[str] = None
    dealer_license: Optional[str] = None
    operating_hours: Optional[str] = None


class DealershipResponse(DealershipBase):
    """Schema for dealership response."""

    id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
