from pydantic import BaseModel
from datetime import date
from typing import Optional

<<<<<<< HEAD
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
=======
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

>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
    class Config:
        from_attributes = True
