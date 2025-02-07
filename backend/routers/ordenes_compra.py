import os
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from crud import ordenes_compra as crud_ordenes_compra
from schemas.ordenes_compra import OrdenCompra as OrdenCompraSchema, OrdenCompraCreate, OrdenCompraUpdate
from models.models import OrdenCompra
from database import get_db
from typing import List
from sqlalchemy import func
from fastapi.responses import FileResponse
from utils.generar_pdf_orden_compra import generar_pdf_orden_compra

router = APIRouter()

@router.post("/", response_model=OrdenCompraSchema)
def crear_orden_compra(orden_compra: OrdenCompraCreate, db: Session = Depends(get_db)):
    try:
        return crud_ordenes_compra.create_orden_compra(db=db, orden_compra=orden_compra, usuario_id=orden_compra.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=dict)
def listar_ordenes_compra(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    ordenes_compra, total = crud_ordenes_compra.get_ordenes_compra(db=db, skip=skip, limit=limit)
    return {"ordenes_compra": [OrdenCompraSchema(**orden_compra.to_dict()) for orden_compra in ordenes_compra], "total": total}

@router.get("/pendientes/total", response_model=dict)
def total_ordenes_compra_pendientes(db: Session = Depends(get_db)):
    total = db.query(func.count(OrdenCompra.orden_compra_id)).filter(OrdenCompra.estado == 'pendiente').scalar()
    return {"total": total}

@router.get("/completadas/total", response_model=dict)
def total_ordenes_compra_completadas(db: Session = Depends(get_db)):
    total = db.query(func.count(OrdenCompra.orden_compra_id)).filter(OrdenCompra.estado == 'completada').scalar()
    return {"total": total}

@router.put("/{orden_compra_id}/estado", response_model=OrdenCompraSchema)
def actualizar_estado_orden_compra(orden_compra_id: int, estado: str, usuario_id: int, db: Session = Depends(get_db)):
    try:
        return crud_ordenes_compra.update_estado_orden_compra(db, orden_compra_id, estado, usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/{orden_compra_id}", response_model=OrdenCompraSchema)
def obtener_orden_compra(orden_compra_id: int, db: Session = Depends(get_db)):
    db_orden_compra = crud_ordenes_compra.get_orden_compra(db=db, orden_compra_id=orden_compra_id)
    if db_orden_compra is None:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    return db_orden_compra

@router.put("/{orden_compra_id}", response_model=OrdenCompraSchema)
def actualizar_orden_compra(orden_compra_id: int, orden_compra: OrdenCompraUpdate, db: Session = Depends(get_db)):
    db_orden_compra = crud_ordenes_compra.update_orden_compra(db=db, orden_compra_id=orden_compra_id, orden_compra=orden_compra, usuario_id=orden_compra.usuario_id)
    if db_orden_compra is None:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    return db_orden_compra

@router.delete("/{orden_compra_id}", response_model=OrdenCompraSchema)
def eliminar_orden_compra(orden_compra_id: int, usuario_id: int, db: Session = Depends(get_db)):
    db_orden_compra = crud_ordenes_compra.delete_orden_compra(db=db, orden_compra_id=orden_compra_id, usuario_id=usuario_id)
    if db_orden_compra is None:
        raise HTTPException(status_code=404, detail="Orden de compra no encontrada")
    return db_orden_compra

@router.get("/generar-pdf/{orden_compra_id}", response_class=FileResponse)
def generar_pdf(orden_compra_id: int, db: Session = Depends(get_db)):
    pdf_path = generar_pdf_orden_compra(orden_compra_id)
    if not os.path.exists(pdf_path):
        raise HTTPException(status_code=404, detail="PDF no encontrado")
    return FileResponse(pdf_path, media_type='application/pdf', filename=f"orden_compra_{orden_compra_id}.pdf")
