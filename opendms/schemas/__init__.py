"""
Pydantic schemas package.
"""

from opendms.schemas.auth import Token, TokenRefresh, UserCreate, UserLogin
from opendms.schemas.customer import CustomerCreate, CustomerResponse, CustomerUpdate
from opendms.schemas.dealership import (
    DealershipCreate,
    DealershipResponse,
    DealershipUpdate,
)
from opendms.schemas.inventory import VehicleCreate, VehicleResponse, VehicleUpdate
from opendms.schemas.sale import SaleCreate, SaleResponse, SaleUpdate
from opendms.schemas.service import (
    ServiceAppointmentCreate,
    ServiceAppointmentResponse,
    ServiceAppointmentUpdate,
)
from opendms.schemas.user import UserCreate, UserResponse, UserUpdate

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
