"""
Security utilities for authentication and authorization.
"""

from datetime import datetime, timedelta
from typing import Any, Optional, Union

from fastapi import HTTPException, status
from jose import jwt
from passlib.context import CryptContext

from mdmsga.core.config import settings

# Password hashing context
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def create_access_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Create JWT access token.

    Args:
        subject: Token subject (usually user ID)
        expires_delta: Token expiration time

    Returns:
        str: JWT token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def create_refresh_token(
    subject: Union[str, Any], expires_delta: timedelta = None
) -> str:
    """
    Create JWT refresh token.

    Args:
        subject: Token subject (usually user ID)
        expires_delta: Token expiration time

    Returns:
        str: JWT refresh token
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    to_encode = {"exp": expire, "sub": str(subject), "type": "refresh"}
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def verify_token(token: str) -> Optional[str]:
    """
    Verify JWT token and return subject.

    Args:
        token: JWT token to verify

    Returns:
        Optional[str]: Token subject if valid, None otherwise
    """
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        subject: str = payload.get("sub")
        if subject is None:
            return None
        return subject
    except jwt.JWTError:
        return None


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify password against hash.

    Args:
        plain_password: Plain text password
        hashed_password: Hashed password

    Returns:
        bool: True if password matches, False otherwise
    """
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash password using bcrypt.

    Args:
        password: Plain text password

    Returns:
        str: Hashed password
    """
    return pwd_context.hash(password)


def authenticate_user(db, email: str, password: str):
    """
    Authenticate user with email and password.

    Args:
        db: Database session
        email: User email
        password: User password

    Returns:
        User object if authentication successful, False otherwise
    """
    from mdmsga.crud.user import get_user_by_email
    from mdmsga.models.user import User

    user = get_user_by_email(db, email=email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def get_current_user(db, token: str):
    """
    Get current user from JWT token.

    Args:
        db: Database session
        token: JWT token

    Returns:
        User object if token valid

    Raises:
        HTTPException: If token invalid or user not found
    """
    from mdmsga.crud.user import get_user
    from mdmsga.models.user import User

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    subject = verify_token(token)
    if subject is None:
        raise credentials_exception

    user = get_user(db, user_id=int(subject))
    if user is None:
        raise credentials_exception

    return user


def get_current_active_user(db, token: str):
    """
    Get current active user from JWT token.

    Args:
        db: Database session
        token: JWT token

    Returns:
        Active User object if token valid

    Raises:
        HTTPException: If token invalid, user not found, or user inactive
    """
    user = get_current_user(db, token)
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user
