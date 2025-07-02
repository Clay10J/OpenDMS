"""
Database models package.
"""

from xdms.models.user import User
from xdms.models.dealership import Dealership
from xdms.models.inventory import Vehicle, VehicleImage
from xdms.models.customer import Customer, CustomerNote
from xdms.models.sale import Sale, SaleItem
from xdms.models.service import ServiceAppointment, ServiceWorkOrder

__all__ = [
    "User",
    "Dealership", 
    "Vehicle",
    "VehicleImage",
    "Customer",
    "CustomerNote",
    "Sale",
    "SaleItem",
    "ServiceAppointment",
    "ServiceWorkOrder",
] 