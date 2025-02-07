from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List
from crud.reportes_entrega import obtener_pedidos, obtener_pedido, obtener_detalles_pedido, registrar_accion
from models.models import Pedido
from schemas.pedidos import Pedido as PedidoSchema
from schemas.detalles_pedidos import DetallePedido as DetallePedidoSchema
from database import get_db
from utils.generar_reporte_entrega import generar_reporte_entrega
from fastapi.responses import FileResponse

router = APIRouter()

@router.get("/pedidos", response_model=dict)
def listar_pedidos(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    pedidos, total = obtener_pedidos(db, skip=skip, limit=limit)
    return {"pedidos": [PedidoSchema(**pedido.to_dict()) for pedido in pedidos], "total": total}

@router.get("/pedidos/{pedido_id}", response_model=PedidoSchema)
def obtener_pedido_endpoint(pedido_id: int, db: Session = Depends(get_db)):
    pedido = obtener_pedido(db, pedido_id)
    if not pedido:
        raise HTTPException(status_code=404, detail="Pedido no encontrado")
    return pedido

@router.get("/pedidos/{pedido_id}/detalles", response_model=List[DetallePedidoSchema])
def listar_detalles_pedido(pedido_id: int, db: Session = Depends(get_db)):
    detalles = obtener_detalles_pedido(db, pedido_id)
    if not detalles:
        raise HTTPException(status_code=404, detail="Detalles del pedido no encontrados")
    return detalles

@router.get("/pedidos/{pedido_id}/generar-reporte", response_class=FileResponse)
def generar_reporte(pedido_id: int, usuario_id: int = Query(...), db: Session = Depends(get_db)):
    try:
        reporte_path = generar_reporte_entrega(pedido_id)
        registrar_accion(db, usuario_id, "Generación de reporte de entrega", f"Reporte de entrega para el pedido ID {pedido_id} generado.")
        return FileResponse(reporte_path, media_type='application/pdf', filename=f'reporte_entrega_{pedido_id}.pdf')
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

