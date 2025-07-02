"""
Authentication schemas.
"""

from typing import Optional

from pydantic import BaseModel, EmailStr

from mdmsga.schemas.user import UserResponse


class Token(BaseModel):
    """Token response schema."""

    access_token: str
    refresh_token: str
    token_type: str
    user: UserResponse


class TokenRefresh(BaseModel):
    """Token refresh request schema."""

    refresh_token: str


class UserLogin(BaseModel):
    """User login request schema."""

    email: EmailStr
    password: str


class UserCreate(BaseModel):
    """User creation request schema."""

    email: EmailStr
    password: str
    first_name: str
    last_name: str
    role: Optional[str] = "viewer"
    phone: Optional[str] = None
    dealership_id: Optional[int] = None
