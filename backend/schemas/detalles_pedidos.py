from pydantic import BaseModel
from typing import Optional

class DetallePedidoBase(BaseModel):
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetallePedidoCreate(DetallePedidoBase):
    pass

class DetallePedidoUpdate(BaseModel):
    cantidad: Optional[int]
    precio_unitario: Optional[float]

class DetallePedido(DetallePedidoBase):
    detalle_id: int

    class Config:
        from_attributes = True
