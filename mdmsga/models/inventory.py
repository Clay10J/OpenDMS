"""
Inventory models for vehicle management.
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

from mdmsga.core.database import Base


class VehicleStatus(str, enum.Enum):
    """Vehicle status enumeration."""

    AVAILABLE = "available"
    SOLD = "sold"
    RESERVED = "reserved"
    IN_TRANSIT = "in_transit"
    SERVICE = "service"
    SOLD_PENDING = "sold_pending"


class Vehicle(Base):
    """Vehicle model for inventory management."""

    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    vin = Column(String(17), unique=True, index=True, nullable=False)
    stock_number = Column(String(50), nullable=False, index=True)
    dealership_id = Column(Integer, ForeignKey("dealerships.id"), nullable=False)

    # Vehicle Information
    year = Column(Integer, nullable=False)
    make = Column(String(100), nullable=False)
    model = Column(String(100), nullable=False)
    trim = Column(String(100), nullable=True)
    body_style = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    interior_color = Column(String(50), nullable=True)

    # Engine and Transmission
    engine = Column(String(100), nullable=True)
    transmission = Column(String(100), nullable=True)
    fuel_type = Column(String(50), nullable=True)
    mileage = Column(Integer, nullable=True)

    # Pricing
    cost_price = Column(Float, nullable=True)
    sale_price = Column(Float, nullable=True)
    msrp = Column(Float, nullable=True)

    # Status and Location
    status = Column(
        Enum(VehicleStatus), default=VehicleStatus.AVAILABLE, nullable=False
    )
    location = Column(String(100), nullable=True)  # Lot location

    # Additional Information
    features = Column(Text, nullable=True)  # JSON string of features
    description = Column(Text, nullable=True)
    notes = Column(Text, nullable=True)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False
    )

    # Relationships
    dealership = relationship("Dealership", back_populates="vehicles")
    images = relationship(
        "VehicleImage", back_populates="vehicle", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"<Vehicle(id={self.id}, vin='{self.vin}', make='{self.make}', model='{self.model}')>"


class VehicleImage(Base):
    """Vehicle image model."""

    __tablename__ = "vehicle_images"

    id = Column(Integer, primary_key=True, index=True)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    image_url = Column(String(500), nullable=False)
    image_type = Column(String(50), nullable=True)  # exterior, interior, etc.
    is_primary = Column(Boolean, default=False, nullable=False)
    sort_order = Column(Integer, default=0, nullable=False)

    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    # Relationships
    vehicle = relationship("Vehicle", back_populates="images")

    def __repr__(self) -> str:
        return f"<VehicleImage(id={self.id}, vehicle_id={self.vehicle_id}, image_url='{self.image_url}')>"
