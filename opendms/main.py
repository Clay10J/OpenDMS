"""
OpenDMS main application entry point.

This module contains the FastAPI application and all route registrations.
"""

import logging
from contextlib import asynccontextmanager
from typing import Any, Dict

import uvicorn
from fastapi import Depends, FastAPI, Form, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session

from opendms.api.v1.api import api_router
from opendms.core.config import settings
from opendms.core.database import Base, engine, get_db
from opendms.core.security import get_current_user
from opendms.models import user

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL), format=settings.LOG_FORMAT
)
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager."""
    print("Starting OpenDMS application...")
    # Create database tables
    Base.metadata.create_all(bind=engine)
    yield
    print("Shutting down OpenDMS application...")


# Create FastAPI application
app = FastAPI(
    title="OpenDMS",
    description="Modern Dealer Management System",
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    lifespan=lifespan,
)

# Mount static files
app.mount("/static", StaticFiles(directory="opendms/static"), name="static")

# Setup Jinja2 templates
templates = Jinja2Templates(directory="opendms/templates")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Set up trusted host middleware
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=["*"] if settings.DEBUG else ["localhost", "127.0.0.1"],
)

# Include API router
app.include_router(api_router, prefix="/api/v1")


# Root route - redirect to login page
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    """Root endpoint."""
    return RedirectResponse(url="/auth/login")


# Dashboard route
@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """Dashboard endpoint."""
    # Get dashboard stats
    stats = {
        "inventory_count": 0,  # TODO: Get from database
        "customer_count": 0,  # TODO: Get from database
        "monthly_sales": 0,  # TODO: Get from database
        "active_service": 0,  # TODO: Get from database
    }

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "current_user": current_user, "stats": stats},
    )


# Inventory routes
@app.get("/inventory", response_class=HTMLResponse)
async def inventory_page(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """Inventory page endpoint."""
    # TODO: Get inventory data from database
    vehicles = []
    makes = []
    pagination = None

    return templates.TemplateResponse(
        "inventory.html",
        {
            "request": request,
            "current_user": current_user,
            "vehicles": vehicles,
            "makes": makes,
            "pagination": pagination,
        },
    )


@app.get("/inventory/new", response_class=HTMLResponse)
async def new_inventory(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """New inventory endpoint."""
    return templates.TemplateResponse(
        "inventory_form.html", {"request": request, "current_user": current_user}
    )


@app.get("/inventory/{vehicle_id}/edit", response_class=HTMLResponse)
async def edit_inventory(
    request: Request,
    vehicle_id: int,
    current_user: user.User = Depends(get_current_user),
):
    """Edit inventory endpoint."""
    # TODO: Get vehicle data from database
    vehicle = None

    return templates.TemplateResponse(
        "inventory_form.html",
        {"request": request, "current_user": current_user, "vehicle": vehicle},
    )


@app.get("/inventory/{vehicle_id}/view", response_class=HTMLResponse)
async def view_inventory(
    request: Request,
    vehicle_id: int,
    current_user: user.User = Depends(get_current_user),
):
    """View inventory endpoint."""
    # TODO: Get vehicle data from database
    vehicle = None

    return templates.TemplateResponse(
        "inventory_view.html",
        {"request": request, "current_user": current_user, "vehicle": vehicle},
    )


# Customer routes
@app.get("/customers", response_class=HTMLResponse)
async def customers_page(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """Customers page endpoint."""
    # TODO: Get customers data from database
    customers = []
    pagination = None

    return templates.TemplateResponse(
        "customers.html",
        {
            "request": request,
            "current_user": current_user,
            "customers": customers,
            "pagination": pagination,
        },
    )


@app.get("/customers/new", response_class=HTMLResponse)
async def new_customer(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """New customer endpoint."""
    return templates.TemplateResponse(
        "customer_form.html", {"request": request, "current_user": current_user}
    )


# Sales routes
@app.get("/sales", response_class=HTMLResponse)
async def sales_page(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """Sales page endpoint."""
    # TODO: Get sales data from database
    sales = []
    pagination = None

    return templates.TemplateResponse(
        "sales.html",
        {
            "request": request,
            "current_user": current_user,
            "sales": sales,
            "pagination": pagination,
        },
    )


@app.get("/sales/new", response_class=HTMLResponse)
async def new_sale(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """New sale endpoint."""
    return templates.TemplateResponse(
        "sale_form.html", {"request": request, "current_user": current_user}
    )


# Service routes
@app.get("/service", response_class=HTMLResponse)
async def service_page(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """Service page endpoint."""
    # TODO: Get service data from database
    service_tickets = []
    pagination = None

    return templates.TemplateResponse(
        "service.html",
        {
            "request": request,
            "current_user": current_user,
            "service_tickets": service_tickets,
            "pagination": pagination,
        },
    )


@app.get("/service/new", response_class=HTMLResponse)
async def new_service(
    request: Request, current_user: user.User = Depends(get_current_user)
):
    """New service endpoint."""
    return templates.TemplateResponse(
        "service_form.html", {"request": request, "current_user": current_user}
    )


# Auth routes
@app.get("/auth/login", response_class=HTMLResponse)
async def login_page(request: Request):
    """Login page endpoint."""
    return templates.TemplateResponse("auth/login.html", {"request": request})


@app.post("/auth/login", response_class=HTMLResponse)
async def login_form(
    request: Request,
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """Login form handler."""
    from datetime import timedelta

    from opendms.core.security import authenticate_user, create_access_token

    # Authenticate user
    user = authenticate_user(db, email=email, password=password)
    if not user:
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Invalid email or password"},
            status_code=401,
        )

    if not getattr(user, "is_active", True):
        return templates.TemplateResponse(
            "auth/login.html",
            {"request": request, "error": "Account is inactive"},
            status_code=401,
        )

    # Create access token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        subject=user.id, expires_delta=access_token_expires
    )

    # Redirect to dashboard with token
    response = RedirectResponse(url="/dashboard", status_code=302)
    response.set_cookie(
        key="access_token",
        value=f"Bearer {access_token}",
        httponly=True,
        max_age=1800,  # 30 minutes
        samesite="lax",
    )
    return response


@app.get("/auth/register", response_class=HTMLResponse)
async def register_page(request: Request):
    """Register page endpoint."""
    return templates.TemplateResponse("auth/register.html", {"request": request})


@app.get("/auth/forgot-password", response_class=HTMLResponse)
async def forgot_password_page(request: Request):
    """Forgot password page endpoint."""
    return templates.TemplateResponse("auth/forgot_password.html", {"request": request})


# Offline page
@app.get("/offline.html", response_class=HTMLResponse)
async def offline_page(request: Request):
    """Offline page endpoint."""
    return templates.TemplateResponse("offline.html", {"request": request})


if __name__ == "__main__":
    uvicorn.run("opendms.main:app", host="0.0.0.0", port=8000, reload=True)
