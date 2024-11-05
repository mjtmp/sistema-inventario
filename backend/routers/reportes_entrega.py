from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.reportes_entrega import (
    get_reporte_entrega, get_reportes_entrega, create_reporte_entrega, 
    update_reporte_entrega, delete_reporte_entrega
)
from ..schemas.reportes_entrega import ReporteEntrega, ReporteEntregaCreate, ReporteEntregaUpdate
from backend.database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
@router.post("/", response_model=ReporteEntrega)
def crear_reporte_entrega(reporte_entrega: ReporteEntregaCreate, db: Session = Depends(get_db)):
    return create_reporte_entrega(db=db, reporte_entrega=reporte_entrega)

@router.get("/", response_model=list[ReporteEntrega])
def listar_reportes_entrega(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_reportes_entrega(db=db, skip=skip, limit=limit)

@router.get("/{entrega_id}", response_model=ReporteEntrega)
def obtener_reporte_entrega(entrega_id: int, db: Session = Depends(get_db)):
    db_reporte_entrega = get_reporte_entrega(db=db, entrega_id=entrega_id)
    if db_reporte_entrega is None:
        raise HTTPException(status_code=404, detail="Reporte de entrega no encontrado")
    return db_reporte_entrega

@router.put("/{entrega_id}", response_model=ReporteEntrega)
def actualizar_reporte_entrega(entrega_id: int, reporte_entrega: ReporteEntregaUpdate, db: Session = Depends(get_db)):
    db_reporte_entrega = update_reporte_entrega(db=db, entrega_id=entrega_id, reporte_entrega=reporte_entrega)
    if db_reporte_entrega is None:
        raise HTTPException(status_code=404, detail="Reporte de entrega no encontrado")
    return db_reporte_entrega

@router.delete("/{entrega_id}", response_model=ReporteEntrega)
def eliminar_reporte_entrega(entrega_id: int, db: Session = Depends(get_db)):
    db_reporte_entrega = delete_reporte_entrega(db=db, entrega_id=entrega_id)
    if db_reporte_entrega is None:
        raise HTTPException(status_code=404, detail="Reporte de entrega no encontrado")
    return db_reporte_entrega
