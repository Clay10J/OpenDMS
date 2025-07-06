"""
Customer schemas for API requests and responses.
"""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class CustomerBase(BaseModel):
    """Base customer schema."""

    first_name: str
    last_name: str
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: str = "USA"
    customer_type: Optional[str] = None
    source: Optional[str] = None
    preferred_contact_method: Optional[str] = None


class CustomerCreate(CustomerBase):
    """Schema for creating a customer."""

    pass


class CustomerUpdate(BaseModel):
    """Schema for updating a customer."""

    first_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    address_line_1: Optional[str] = None
    address_line_2: Optional[str] = None
    city: Optional[str] = None
    state: Optional[str] = None
    zip_code: Optional[str] = None
    country: Optional[str] = None
    customer_type: Optional[str] = None
    source: Optional[str] = None
    preferred_contact_method: Optional[str] = None


class CustomerResponse(CustomerBase):
    """Schema for customer response."""

    id: int
    dealership_id: int
    is_active: bool
    is_verified: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
