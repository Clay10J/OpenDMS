"""
Service schemas for API requests and responses.
"""

from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel


class ServiceAppointmentBase(BaseModel):
    """Base service appointment schema."""

    customer_id: int
    vehicle_id: int
    service_advisor_id: int
    appointment_date: datetime
    service_type: str
    description: Optional[str] = None
    estimated_cost: Optional[Decimal] = None
    estimated_duration: Optional[int] = None
    priority: str = "normal"
    status: str = "scheduled"
    notes: Optional[str] = None


class ServiceAppointmentCreate(ServiceAppointmentBase):
    """Schema for creating a service appointment."""

    pass


class ServiceAppointmentUpdate(BaseModel):
    """Schema for updating a service appointment."""

    customer_id: Optional[int] = None
    vehicle_id: Optional[int] = None
    service_advisor_id: Optional[int] = None
    appointment_date: Optional[datetime] = None
    service_type: Optional[str] = None
    description: Optional[str] = None
    estimated_cost: Optional[Decimal] = None
    estimated_duration: Optional[int] = None
    priority: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None


class ServiceAppointmentResponse(ServiceAppointmentBase):
    """Schema for service appointment response."""

    id: int
    dealership_id: int
    actual_cost: Optional[Decimal] = None
    actual_duration: Optional[int] = None
    completed_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
