from pydantic import BaseModel
from typing import Optional

class DetalleOrdenCompraBase(BaseModel):
    orden_compra_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetalleOrdenCompraCreate(DetalleOrdenCompraBase):
    pass

class DetalleOrdenCompraUpdate(BaseModel):
    cantidad: Optional[int]
    precio_unitario: Optional[float]

class DetalleOrdenCompra(DetalleOrdenCompraBase):
    detalle_id: int

    class Config:
        from_attributes = True
