from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..crud.pedidos import get_pedido, get_pedidos, create_pedido, update_pedido, delete_pedido
from ..schemas.pedidos import Pedido, PedidoCreate, PedidoUpdate
from backend.database import SessionLocal

router = APIRouter()

# Dependencia para obtener la sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=Pedido)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    return create_pedido(db=db, pedido=pedido)

@router.get("/", response_model=List[Pedido])
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return get_pedidos(db=db, skip=skip, limit=limit)

@router.get("/{pedido_id}", response_model=Pedido)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.put("/{pedido_id}", response_model=Pedido)
def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = update_pedido(db=db, pedido_id=pedido_id, pedido=pedido)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.delete("/{pedido_id}", response_model=Pedido)
def eliminar_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = delete_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido
