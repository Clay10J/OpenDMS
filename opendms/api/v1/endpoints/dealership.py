"""
Dealership endpoints for API v1.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from opendms.core.database import get_db
from opendms.models.dealership import Dealership
from opendms.schemas.dealership import (
    DealershipCreate,
    DealershipResponse,
    DealershipUpdate,
)

router = APIRouter()


@router.get("/", response_model=List[DealershipResponse])
def get_dealerships(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all dealerships."""
    dealerships = db.query(Dealership).offset(skip).limit(limit).all()
    return dealerships


@router.post("/", response_model=DealershipResponse)
def create_dealership(
    dealership: DealershipCreate,
    db: Session = Depends(get_db),
):
    """Create a new dealership."""
    db_dealership = Dealership(**dealership.model_dump())
    db.add(db_dealership)
    db.commit()
    db.refresh(db_dealership)
    return db_dealership


@router.get("/{dealership_id}", response_model=DealershipResponse)
def get_dealership(
    dealership_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific dealership by ID."""
    dealership = db.query(Dealership).filter(Dealership.id == dealership_id).first()
    if dealership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dealership not found"
        )
    return dealership


@router.put("/{dealership_id}", response_model=DealershipResponse)
def update_dealership(
    dealership_id: int,
    dealership: DealershipUpdate,
    db: Session = Depends(get_db),
):
    """Update a dealership."""
    db_dealership = db.query(Dealership).filter(Dealership.id == dealership_id).first()
    if db_dealership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dealership not found"
        )

    update_data = dealership.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_dealership, field, value)

    db.commit()
    db.refresh(db_dealership)
    return db_dealership


@router.delete("/{dealership_id}")
def delete_dealership(
    dealership_id: int,
    db: Session = Depends(get_db),
):
    """Delete a dealership."""
    dealership = db.query(Dealership).filter(Dealership.id == dealership_id).first()
    if dealership is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Dealership not found"
        )

    db.delete(dealership)
    db.commit()
    return {"message": "Dealership deleted successfully"}
