from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .detalles_pedidos import DetallePedido

class PedidoBase(BaseModel):
    cliente_id: int
    fecha_pedido: date
    estado: str

class PedidoCreate(PedidoBase):
    detalles: List[DetallePedido]
    usuario_id: int  # Asegurar que usuario_id está incluido

class PedidoUpdate(BaseModel):
    estado: Optional[str]
    usuario_id: int  # Incluir usuario_id

class Pedido(PedidoBase):
    pedido_id: int
    detalles: List[DetallePedido] = []

    class Config:
        from_attributes = True

