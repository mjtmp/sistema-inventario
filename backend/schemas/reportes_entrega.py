from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReporteEntregaBase(BaseModel):
    pedido_id: int
    fecha_entrega: date
    estado: str

class ReporteEntregaCreate(ReporteEntregaBase):
    pass

class ReporteEntregaUpdate(BaseModel):
    fecha_entrega: Optional[date]
    estado: Optional[str]

class ReporteEntrega(ReporteEntregaBase):
    entrega_id: int

    class Config:
        from_attributes = True
