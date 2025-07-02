"""
Pydantic schemas package.
"""

from xdms.schemas.auth import Token, TokenRefresh, UserLogin, UserCreate
from xdms.schemas.user import UserResponse, UserCreate, UserUpdate
from xdms.schemas.dealership import DealershipResponse, DealershipCreate, DealershipUpdate
from xdms.schemas.inventory import VehicleResponse, VehicleCreate, VehicleUpdate
from xdms.schemas.customer import CustomerResponse, CustomerCreate, CustomerUpdate
from xdms.schemas.sale import SaleResponse, SaleCreate, SaleUpdate
from xdms.schemas.service import ServiceAppointmentResponse, ServiceAppointmentCreate, ServiceAppointmentUpdate

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