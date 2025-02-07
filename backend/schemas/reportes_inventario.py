from pydantic import BaseModel
from datetime import date
from typing import Optional

# Esquema base para reportes de inventario.
class ReporteInventarioBase(BaseModel):
    fecha: date  # Fecha del reporte.
    producto_id: int  # ID del producto relacionado con el inventario.
    stock: int  # Cantidad en stock registrada.

# Esquema para crear un reporte de inventario.
class ReporteInventarioCreate(ReporteInventarioBase):
    pass  # Utiliza los mismos campos del esquema base.

# Esquema para actualizar un reporte de inventario.
class ReporteInventarioUpdate(BaseModel):
    fecha: Optional[date]  # La fecha puede ser opcional al actualizar.
    stock: Optional[int]  # El stock también es opcional.

# Esquema para la representación completa de un reporte de inventario.
class ReporteInventario(ReporteInventarioBase):
    reporte_id: int  # ID único del reporte.

    # Configuración para permitir mapeo directo desde los modelos ORM.
    class Config:
        from_attributes = True
