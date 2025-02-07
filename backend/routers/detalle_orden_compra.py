from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import detalle_orden_compra as crud_detalle_orden_compra
from schemas.detalle_orden_compra import DetalleOrdenCompraCreate, DetalleOrdenCompraUpdate, DetalleOrdenCompra
from database import get_db
from typing import List

router = APIRouter()

@router.get("/{detalle_id}", response_model=DetalleOrdenCompra)
def read_detalle_orden_compra(detalle_id: int, db: Session = Depends(get_db)):
    db_detalle = crud_detalle_orden_compra.get_detalle_orden_compra(db, detalle_id)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de orden de compra no encontrado")
    return db_detalle

@router.get("/", response_model=List[DetalleOrdenCompra])
def read_detalles_orden_compra(orden_compra_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_detalle_orden_compra.get_detalles_orden_compra(db, orden_compra_id, skip, limit)

@router.post("/", response_model=DetalleOrdenCompra)
def create_detalle_orden_compra(detalle: DetalleOrdenCompraCreate, db: Session = Depends(get_db)):
    return crud_detalle_orden_compra.create_detalle_orden_compra(db, detalle)

@router.put("/{detalle_id}", response_model=DetalleOrdenCompra)
def update_detalle_orden_compra(detalle_id: int, detalle: DetalleOrdenCompraUpdate, db: Session = Depends(get_db)):
    db_detalle = crud_detalle_orden_compra.update_detalle_orden_compra(db, detalle_id, detalle)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de orden de compra no encontrado")
    return db_detalle

@router.delete("/{detalle_id}", response_model=DetalleOrdenCompra)
def delete_detalle_orden_compra(detalle_id: int, db: Session = Depends(get_db)):
    db_detalle = crud_detalle_orden_compra.delete_detalle_orden_compra(db, detalle_id)
    if not db_detalle:
        raise HTTPException(status_code=404, detail="Detalle de orden de compra no encontrado")
    return db_detalle
