from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .detalles_pedidos import DetallePedido  # Asegúrate de tener este esquema en schemas/detalles_pedidos.py

class PedidoBase(BaseModel):
    cliente_id: int
    fecha: date
    total: float

class PedidoCreate(PedidoBase):
    pass

class PedidoUpdate(PedidoBase):
    pass

class Pedido(PedidoBase):
    pedido_id: int
    detalles: List[DetallePedido] = []

    class Config:
        from_attributes = True
