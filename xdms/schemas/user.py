"""
User schemas.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, ConfigDict

from xdms.models.user import UserRole


class UserBase(BaseModel):
    """Base user schema."""
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    role: Optional[UserRole] = None
    phone: Optional[str] = None
    dealership_id: Optional[int] = None


class UserCreate(UserBase):
    """User creation schema."""
    email: EmailStr
    password: str
    first_name: str
    last_name: str


class UserUpdate(UserBase):
    """User update schema."""
    password: Optional[str] = None


class UserResponse(UserBase):
    """User response schema."""
    id: int
    is_active: bool
    is_verified: bool
    avatar_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    last_login: Optional[datetime] = None
    
    model_config = ConfigDict(from_attributes=True)
    
    @property
    def full_name(self) -> str:
        """Get user's full name."""
        return f"{self.first_name} {self.last_name}" 