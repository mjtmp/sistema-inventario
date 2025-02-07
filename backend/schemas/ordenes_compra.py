from pydantic import BaseModel
from datetime import date
from typing import List, Optional
from .detalle_orden_compra import DetalleOrdenCompraCreate, DetalleOrdenCompra

class OrdenCompraBase(BaseModel):
    proveedor_id: int
    fecha_orden: date
    estado: str

class OrdenCompraCreate(OrdenCompraBase):
    detalles: List[DetalleOrdenCompraCreate]
    usuario_id: int

class OrdenCompraUpdate(BaseModel):
    estado: Optional[str]
    usuario_id: int

class OrdenCompra(OrdenCompraBase):
    orden_compra_id: int
    detalles: List[DetalleOrdenCompra] = []

    class Config:
        from_attributes = True

