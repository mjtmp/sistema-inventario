<<<<<<< HEAD
from pydantic import BaseModel  # Base para los esquemas de validación
from datetime import date  # Manejo de fechas
from typing import Optional  # Soporte para campos opcionales

# Base del esquema para reporte de entrega
class ReporteEntregaBase(BaseModel):
    pedido_id: int  # ID del pedido relacionado
    fecha_entrega: date  # Fecha de la entrega
    estado: str  # Estado actual del reporte

# Esquema para la creación de un reporte de entrega
class ReporteEntregaCreate(ReporteEntregaBase):
    pass  # Hereda todos los campos de ReporteEntregaBase

# Esquema para la actualización de un reporte de entrega
class ReporteEntregaUpdate(BaseModel):
    fecha_entrega: Optional[date]  # Fecha de entrega opcional
    estado: Optional[str]  # Estado opcional

# Esquema completo de reporte de entrega (incluye ID)
class ReporteEntrega(ReporteEntregaBase):
    entrega_id: int  # ID único del reporte

    class Config:
        from_attributes = True  # Permite convertir desde objetos SQLAlchemy

=======
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
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
