from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.models import Pedido
from crud.pedidos import (
    get_pedido, get_pedidos, create_pedido, update_pedido, delete_pedido, get_pedidos_completados
)
from schemas.pedidos import Pedido as PedidoSchema, PedidoCreate, PedidoUpdate
from database import SessionLocal
from typing import List, Optional
from sqlalchemy import func
from fastapi.responses import FileResponse
from utils.generar_pedido import generar_pedido, generate_unique_order_number

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/completados", response_model=List[PedidoSchema])
def listar_pedidos_completados(db: Session = Depends(get_db)):
    pedidos = get_pedidos_completados(db)
    return pedidos

# Ruta para crear un pedido
@router.post("/", response_model=PedidoSchema)
def crear_pedido(pedido: PedidoCreate, db: Session = Depends(get_db)):
    try:
        return create_pedido(db=db, pedido=pedido, usuario_id=pedido.usuario_id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

# Ruta para listar pedidos con paginación
@router.get("/", response_model=dict)
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pedidos, total = get_pedidos(db=db, skip=skip, limit=limit)
    return {"pedidos": [PedidoSchema(**pedido.to_dict()) for pedido in pedidos], "total": total}

@router.get("/pendientes/total", response_model=dict)
def total_pedidos_pendientes(db: Session = Depends(get_db)):
    total = db.query(func.count(Pedido.pedido_id)).filter(Pedido.estado == 'pendiente').scalar()
    return {"total": total}

@router.get("/entregados/total", response_model=dict)
def total_pedidos_entregados(db: Session = Depends(get_db)):
    total = db.query(func.count(Pedido.pedido_id)).filter(Pedido.estado == 'completado').scalar()
    return {"total": total}

@router.get("/{pedido_id}", response_model=PedidoSchema)
def obtener_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.put("/{pedido_id}", response_model=PedidoSchema)
def actualizar_pedido(pedido_id: int, pedido: PedidoUpdate, db: Session = Depends(get_db)):
    db_pedido = update_pedido(db=db, pedido_id=pedido_id, pedido=pedido, usuario_id=pedido.usuario_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

@router.delete("/{pedido_id}", response_model=PedidoSchema)
def eliminar_pedido(pedido_id: int, usuario_id: int, db: Session = Depends(get_db)):
    db_pedido = delete_pedido(db=db, pedido_id=pedido_id, usuario_id=usuario_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return db_pedido

# Ruta para generar el PDF de un pedido
@router.get("/{pedido_id}/generate_pdf", response_class=FileResponse)
def generar_pdf_pedido(pedido_id: int, db: Session = Depends(get_db)):
    db_pedido = get_pedido(db=db, pedido_id=pedido_id)
    if db_pedido is None:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
    cliente = {
        "nombre": db_pedido.cliente.nombre,
        "telefono": db_pedido.cliente.telefono,
        "email": db_pedido.cliente.email,
        "direccion": db_pedido.cliente.direccion
    }

    pedido_info = {
        "numero": db_pedido.pedido_id,
        "estado": db_pedido.estado,
    }

    productos = [
        {
            "cantidad": detalle.cantidad,
            "descripcion": detalle.producto.nombre,
            "precio_unitario": detalle.precio_unitario,
            "tiene_iva": detalle.producto.tiene_iva
        }
        for detalle in db_pedido.detalles
    ]

    metodos_pago = [
        "Transferencia Bancaria", 
        "Tarjeta de Crédito",
        "Tarjeta de Débito",
        "Pago en Efectivo"
    ]

    pdf_path = generar_pedido(cliente, pedido_info, productos, metodos_pago)

    return FileResponse(pdf_path, filename=f"Pedido_{pedido_info['numero']}.pdf", media_type='application/pdf')


