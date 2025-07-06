"""
Service endpoints for API v1.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from opendms.core.database import get_db
from opendms.models.service import ServiceAppointment
from opendms.schemas.service import (
    ServiceAppointmentCreate,
    ServiceAppointmentResponse,
    ServiceAppointmentUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[ServiceAppointmentResponse])
def get_service_appointments(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all service appointments."""
    appointments = db.query(ServiceAppointment).offset(skip).limit(limit).all()
    return appointments


@router.post("/", response_model=ServiceAppointmentResponse)
def create_service_appointment(
    appointment: ServiceAppointmentCreate,
    db: Session = Depends(get_db),
):
    """Create a new service appointment."""
    db_appointment = ServiceAppointment(**appointment.model_dump())
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.get("/{appointment_id}", response_model=ServiceAppointmentResponse)
def get_service_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific service appointment by ID."""
    appointment = (
        db.query(ServiceAppointment)
        .filter(ServiceAppointment.id == appointment_id)
        .first()
    )
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service appointment not found",
        )
    return appointment


@router.put("/{appointment_id}", response_model=ServiceAppointmentResponse)
def update_service_appointment(
    appointment_id: int,
    appointment: ServiceAppointmentUpdate,
    db: Session = Depends(get_db),
):
    """Update a service appointment."""
    db_appointment = (
        db.query(ServiceAppointment)
        .filter(ServiceAppointment.id == appointment_id)
        .first()
    )
    if db_appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service appointment not found",
        )

    update_data = appointment.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_appointment, field, value)

    db.commit()
    db.refresh(db_appointment)
    return db_appointment


@router.delete("/{appointment_id}")
def delete_service_appointment(
    appointment_id: int,
    db: Session = Depends(get_db),
):
    """Delete a service appointment."""
    appointment = (
        db.query(ServiceAppointment)
        .filter(ServiceAppointment.id == appointment_id)
        .first()
    )
    if appointment is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Service appointment not found",
        )

    db.delete(appointment)
    db.commit()
    return {"message": "Service appointment deleted successfully"}
