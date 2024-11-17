from pydantic import BaseModel
from typing import Optional

class FacturaProductoBase(BaseModel):
    factura_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class FacturaProductoCreate(FacturaProductoBase):
    pass

class FacturaProductoUpdate(FacturaProductoBase):
    pass

class FacturaProducto(FacturaProductoBase):
    id: int
    monto_total: Optional[float] = None

    class Config:
        from_attributes = True
