from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.detalles_pedidos import (
    get_detalle_pedido, get_detalles_pedidos, create_detalle_pedido, 
    update_detalle_pedido, delete_detalle_pedido
)
from ..schemas.detalles_pedidos import DetallePedido, DetallePedidoCreate, DetallePedidoUpdate
from backend.database import SessionLocal

router = APIRouter()
# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=DetallePedido)
def crear_detalle_pedido(detalle_pedido: DetallePedidoCreate, db: Session = Depends(get_db)):
    return create_detalle_pedido(db=db, detalle_pedido=detalle_pedido)

@router.get("/", response_model=list[DetallePedido])
def listar_detalles_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_detalles_pedidos(db=db, skip=skip, limit=limit)

@router.get("/{detalle_id}", response_model=DetallePedido)
def obtener_detalle_pedido(detalle_id: int, db: Session = Depends(get_db)):
    db_detalle_pedido = get_detalle_pedido(db=db, detalle_id=detalle_id)
    if db_detalle_pedido is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return db_detalle_pedido

@router.put("/{detalle_id}", response_model=DetallePedido)
def actualizar_detalle_pedido(detalle_id: int, detalle_pedido: DetallePedidoUpdate, db: Session = Depends(get_db)):
    db_detalle_pedido = update_detalle_pedido(db=db, detalle_id=detalle_id, detalle_pedido=detalle_pedido)
    if db_detalle_pedido is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return db_detalle_pedido

@router.delete("/{detalle_id}", response_model=DetallePedido)
def eliminar_detalle_pedido(detalle_id: int, db: Session = Depends(get_db)):
    db_detalle_pedido = delete_detalle_pedido(db=db, detalle_id=detalle_id)
    if db_detalle_pedido is None:
        raise HTTPException(status_code=404, detail="Detalle de pedido no encontrado")
    return db_detalle_pedido
