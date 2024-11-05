from pydantic import BaseModel
from datetime import date
from typing import Optional

class ReporteInventarioBase(BaseModel):
    fecha: date
    producto_id: int
    stock: int

class ReporteInventarioCreate(ReporteInventarioBase):
    pass

class ReporteInventarioUpdate(BaseModel):
    fecha: Optional[date]
    stock: Optional[int]

class ReporteInventario(ReporteInventarioBase):
    reporte_id: int

    class Config:
        from_attributes = True
