"""
User CRUD operations.
"""

from typing import Optional

from sqlalchemy.orm import Session

from opendms.core.security import get_password_hash
from opendms.models.user import User
from opendms.schemas.auth import UserCreate


def get_user(db: Session, user_id: int) -> Optional[User]:
    """Get user by ID."""
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Get user by email."""
    return db.query(User).filter(User.email == email).first()


def create_user(db: Session, obj_in: UserCreate) -> User:
    """Create a new user."""
    db_obj = User(
        email=obj_in.email,
        hashed_password=get_password_hash(obj_in.password),
        first_name=obj_in.first_name,
        last_name=obj_in.last_name,
        role=obj_in.role,
        phone=obj_in.phone,
        dealership_id=obj_in.dealership_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj
