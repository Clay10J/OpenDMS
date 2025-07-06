"""
Customer models for CRM functionality.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship

from opendms.core.database import Base


class Customer(Base):
    """Customer model for CRM functionality."""

    __tablename__ = "customers"

    id = Column(Integer, primary_key=True, index=True)
    dealership_id = Column(Integer, ForeignKey("dealerships.id"), nullable=False)

    # Personal Information
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    email = Column(String(255), nullable=True, index=True)
    phone = Column(String(20), nullable=True)
    date_of_birth = Column(DateTime, nullable=True)

    # Address
    address_line_1 = Column(String(255), nullable=True)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=True)
    state = Column(String(2), nullable=True)
    zip_code = Column(String(10), nullable=True)
    country = Column(String(100), default="USA", nullable=True)

    # Customer Information
    customer_type = Column(String(50), nullable=True)  # new, returning, prospect
    source = Column(String(100), nullable=True)  # walk-in, referral, website, etc.
    preferred_contact_method = Column(String(50), nullable=True)  # email, phone, text

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    dealership = relationship("Dealership", back_populates="customers")
    notes = relationship(
        "CustomerNote", back_populates="customer", cascade="all, delete-orphan"
    )
    sales = relationship("Sale", back_populates="customer")
    service_appointments = relationship("ServiceAppointment", back_populates="customer")

    @property
    def full_name(self) -> str:
        """Get customer's full name."""
        return f"{self.first_name} {self.last_name}"

    def __repr__(self) -> str:
        return (
            f"<Customer(id={self.id}, name='{self.full_name}', email='{self.email}')>"
        )


class CustomerNote(Base):
    """Customer note model for tracking interactions."""

    __tablename__ = "customer_notes"

    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    # Note Information
    title = Column(String(255), nullable=True)
    content = Column(Text, nullable=False)
    note_type = Column(String(50), nullable=True)  # call, email, meeting, etc.

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    customer = relationship("Customer", back_populates="notes")
    user = relationship("User")

    def __repr__(self) -> str:
        return f"<CustomerNote(id={self.id}, customer_id={self.customer_id}, title='{self.title}')>"
