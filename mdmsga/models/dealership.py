"""
Dealership model for managing dealership information.
"""

from datetime import datetime
from typing import Optional

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    String,
    Text,
)
from sqlalchemy.orm import relationship

from mdmsga.core.database import Base


class Dealership(Base):
    """Dealership model for managing dealership information."""

    __tablename__ = "dealerships"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    legal_name = Column(String(255), nullable=True)
    dealer_number = Column(String(50), unique=True, nullable=False, index=True)

    # Contact Information
    phone = Column(String(20), nullable=True)
    email = Column(String(255), nullable=True)
    website = Column(String(500), nullable=True)

    # Address
    address_line_1 = Column(String(255), nullable=False)
    address_line_2 = Column(String(255), nullable=True)
    city = Column(String(100), nullable=False)
    state = Column(String(2), nullable=False)
    zip_code = Column(String(10), nullable=False)
    country = Column(String(100), default="USA", nullable=False)

    # Business Information
    tax_id = Column(String(50), nullable=True)
    business_license = Column(String(100), nullable=True)
    dealer_license = Column(String(100), nullable=True)

    # Operating Hours (stored as JSON in production)
    operating_hours = Column(Text, nullable=True)  # JSON string

    # Status
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    users = relationship("User", back_populates="dealership")

    def __repr__(self) -> str:
        return f"<Dealership(id={self.id}, name='{self.name}', dealer_number='{self.dealer_number}')>"
