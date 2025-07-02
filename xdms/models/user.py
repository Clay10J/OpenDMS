"""
User model for authentication and authorization.
"""

from datetime import datetime
from typing import Optional
from sqlalchemy import Boolean, Column, DateTime, Integer, String, Text, Enum
from sqlalchemy.orm import relationship
import enum

from xdms.core.database import Base


class UserRole(str, enum.Enum):
    """User roles enumeration."""
    SUPER_ADMIN = "super_admin"
    DEALER_ADMIN = "dealer_admin"
    SALES_MANAGER = "sales_manager"
    SALES_PERSON = "sales_person"
    SERVICE_MANAGER = "service_manager"
    SERVICE_TECHNICIAN = "service_technician"
    FINANCE_MANAGER = "finance_manager"
    INVENTORY_MANAGER = "inventory_manager"
    CUSTOMER_SERVICE = "customer_service"
    VIEWER = "viewer"


class User(Base):
    """User model for authentication and authorization."""
    
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.VIEWER, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_verified = Column(Boolean, default=False, nullable=False)
    phone = Column(String(20), nullable=True)
    avatar_url = Column(String(500), nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    last_login = Column(DateTime, nullable=True)
    
    # Relationships
    dealership_id = Column(Integer, nullable=True)  # Foreign key to dealership
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}"
    
    @property
    def is_admin(self) -> bool:
        """Check if user is an admin."""
        return self.role in [UserRole.SUPER_ADMIN, UserRole.DEALER_ADMIN]
    
    def __repr__(self) -> str:
        return f"<User(id={self.id}, email='{self.email}', role='{self.role}')>" 