"""
Sales endpoints for API v1.
"""

from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from opendms.core.database import get_db
from opendms.models.sale import Sale
from opendms.schemas.sale import SaleCreate, SaleResponse, SaleUpdate

router = APIRouter()


@router.get("/", response_model=List[SaleResponse])
def get_sales(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db),
):
    """Get all sales."""
    sales = db.query(Sale).offset(skip).limit(limit).all()
    return sales


@router.post("/", response_model=SaleResponse)
def create_sale(
    sale: SaleCreate,
    db: Session = Depends(get_db),
):
    """Create a new sale."""
    db_sale = Sale(**sale.model_dump())
    db.add(db_sale)
    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.get("/{sale_id}", response_model=SaleResponse)
def get_sale(
    sale_id: int,
    db: Session = Depends(get_db),
):
    """Get a specific sale by ID."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found"
        )
    return sale


@router.put("/{sale_id}", response_model=SaleResponse)
def update_sale(
    sale_id: int,
    sale: SaleUpdate,
    db: Session = Depends(get_db),
):
    """Update a sale."""
    db_sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if db_sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found"
        )

    update_data = sale.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_sale, field, value)

    db.commit()
    db.refresh(db_sale)
    return db_sale


@router.delete("/{sale_id}")
def delete_sale(
    sale_id: int,
    db: Session = Depends(get_db),
):
    """Delete a sale."""
    sale = db.query(Sale).filter(Sale.id == sale_id).first()
    if sale is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Sale not found"
        )

    db.delete(sale)
    db.commit()
    return {"message": "Sale deleted successfully"}
