"""
Service models for service management.
"""

import enum
from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Enum,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from opendms.core.database import Base


class AppointmentStatus(str, enum.Enum):
    """Appointment status enumeration."""

    SCHEDULED = "scheduled"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"


class WorkOrderStatus(str, enum.Enum):
    """Work order status enumeration."""

    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    ON_HOLD = "on_hold"


class ServiceAppointment(Base):
    """Service appointment model."""

    __tablename__ = "service_appointments"

    id = Column(Integer, primary_key=True, index=True)
    appointment_number = Column(String(50), unique=True, index=True, nullable=False)
    dealership_id = Column(Integer, ForeignKey("dealerships.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    service_advisor_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Appointment Information
    appointment_date = Column(DateTime, nullable=False)
    estimated_duration = Column(Integer, nullable=True)  # minutes
    status = Column(
        Enum(AppointmentStatus), default=AppointmentStatus.SCHEDULED, nullable=False
    )

    # Service Information
    service_type = Column(
        String(100), nullable=True
    )  # maintenance, repair, warranty, etc.
    description = Column(Text, nullable=True)
    customer_concerns = Column(Text, nullable=True)

    # Additional Information
    notes = Column(Text, nullable=True)
    reminder_sent = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    dealership = relationship("Dealership", back_populates="service_appointments")
    customer = relationship("Customer", back_populates="service_appointments")
    vehicle = relationship("Vehicle", back_populates="service_appointments")
    service_advisor = relationship("User")
    work_orders = relationship(
        "ServiceWorkOrder", back_populates="appointment", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<ServiceAppointment(id={self.id}, appointment_number='{self.appointment_number}', status='{self.status}')>"


class ServiceWorkOrder(Base):
    """Service work order model."""

    __tablename__ = "service_work_orders"

    id = Column(Integer, primary_key=True, index=True)
    work_order_number = Column(String(50), unique=True, index=True, nullable=False)
    appointment_id = Column(
        Integer, ForeignKey("service_appointments.id"), nullable=False
    )
    technician_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    # Work Order Information
    status = Column(
        Enum(WorkOrderStatus), default=WorkOrderStatus.PENDING, nullable=False
    )
    estimated_hours = Column(Float, nullable=True)
    actual_hours = Column(Float, nullable=True)

    # Service Details
    labor_rate = Column(Float, nullable=True)
    labor_cost = Column(Float, nullable=True)
    parts_cost = Column(Float, nullable=True)
    total_cost = Column(Float, nullable=True)

    # Work Information
    work_description = Column(Text, nullable=True)
    work_performed = Column(Text, nullable=True)
    recommendations = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    appointment = relationship("ServiceAppointment", back_populates="work_orders")
    technician = relationship("User")

    def __repr__(self) -> str:
        return f"<ServiceWorkOrder(id={self.id}, work_order_number='{self.work_order_number}', status='{self.status}')>"
