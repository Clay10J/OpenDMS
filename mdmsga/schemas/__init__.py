"""
Pydantic schemas package.
"""

from mdmsga.schemas.auth import Token, TokenRefresh, UserCreate, UserLogin
from mdmsga.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from mdmsga.schemas.dealership import (
    DealershipCreate,
    DealershipResponse,
    DealershipUpdate,
)
from mdmsga.schemas.inventory import VehicleCreate, VehicleResponse, VehicleUpdate
from mdmsga.schemas.sale import SaleCreate, SaleResponse, SaleUpdate
from mdmsga.schemas.service import (
    ServiceAppointmentCreate,
    ServiceAppointmentResponse,
    ServiceAppointmentUpdate,
)
from mdmsga.schemas.user import UserCreate, UserResponse, UserUpdate

__all__ = [
    "Token",
    "TokenRefresh",
    "UserLogin",
    "UserCreate",
    "UserResponse",
    "UserUpdate",
    "DealershipResponse",
    "DealershipCreate",
    "DealershipUpdate",
    "VehicleResponse",
    "VehicleCreate",
    "VehicleUpdate",
    "CustomerResponse",
    "CustomerCreate",
    "CustomerUpdate",
    "SaleResponse",
    "SaleCreate",
    "SaleUpdate",
    "ServiceAppointmentResponse",
    "ServiceAppointmentCreate",
    "ServiceAppointmentUpdate",
]
