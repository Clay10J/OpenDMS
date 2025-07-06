"""
Database models package.
"""

from opendms.models.customer import Customer, CustomerNote
from opendms.models.dealership import Dealership
from opendms.models.inventory import Vehicle, VehicleImage
from opendms.models.sale import Sale, SaleItem
from opendms.models.service import ServiceAppointment, ServiceWorkOrder
from opendms.models.user import User

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
