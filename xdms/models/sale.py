"""
Sale models for sales management.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Float, ForeignKey, Enum
from sqlalchemy.orm import relationship
import enum

from xdms.core.database import Base


class SaleStatus(str, enum.Enum):
    """Sale status enumeration."""
    PENDING = "pending"
    APPROVED = "approved"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    DELIVERED = "delivered"


class Sale(Base):
    """Sale model for sales management."""
    
    __tablename__ = "sales"
    
    id = Column(Integer, primary_key=True, index=True)
    sale_number = Column(String(50), unique=True, index=True, nullable=False)
    dealership_id = Column(Integer, ForeignKey("dealerships.id"), nullable=False)
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    sales_person_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    vehicle_id = Column(Integer, ForeignKey("vehicles.id"), nullable=False)
    
    # Sale Information
    sale_date = Column(DateTime, nullable=False)
    status = Column(Enum(SaleStatus), default=SaleStatus.PENDING, nullable=False)
    
    # Pricing
    vehicle_price = Column(Float, nullable=False)
    trade_in_value = Column(Float, nullable=True)
    down_payment = Column(Float, nullable=True)
    finance_amount = Column(Float, nullable=True)
    total_amount = Column(Float, nullable=False)
    
    # Financing
    finance_company = Column(String(100), nullable=True)
    interest_rate = Column(Float, nullable=True)
    term_months = Column(Integer, nullable=True)
    monthly_payment = Column(Float, nullable=True)
    
    # Additional Information
    notes = Column(Text, nullable=True)
    documents = Column(Text, nullable=True)  # JSON string of document URLs
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    dealership = relationship("Dealership", back_populates="sales")
    customer = relationship("Customer", back_populates="sales")
    sales_person = relationship("User")
    vehicle = relationship("Vehicle", back_populates="sales")
    items = relationship("SaleItem", back_populates="sale", cascade="all, delete-orphan")
    
    def __repr__(self) -> str:
        return f"<Sale(id={self.id}, sale_number='{self.sale_number}', status='{self.status}')>"


class SaleItem(Base):
    """Sale item model for additional products/services."""
    
    __tablename__ = "sale_items"
    
    id = Column(Integer, primary_key=True, index=True)
    sale_id = Column(Integer, ForeignKey("sales.id"), nullable=False)
    
    # Item Information
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)
    
    # Item Type
    item_type = Column(String(50), nullable=True)  # warranty, service, accessory, etc.
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    sale = relationship("Sale", back_populates="items")
    
    def __repr__(self) -> str:
        return f"<SaleItem(id={self.id}, name='{self.name}', quantity={self.quantity})>" 