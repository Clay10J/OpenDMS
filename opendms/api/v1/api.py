"""
Main API router for v1 endpoints.
"""

from fastapi import APIRouter

from opendms.api.v1.endpoints import (
    auth,
    customers,
    dealerships,
    inventory,
    sales,
    service,
    users,
)

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(users.router, prefix="/users", tags=["users"])
api_router.include_router(
    dealerships.router, prefix="/dealerships", tags=["dealerships"]
)
api_router.include_router(inventory.router, prefix="/inventory", tags=["inventory"])
api_router.include_router(customers.router, prefix="/customers", tags=["customers"])
api_router.include_router(sales.router, prefix="/sales", tags=["sales"])
api_router.include_router(service.router, prefix="/service", tags=["service"])
