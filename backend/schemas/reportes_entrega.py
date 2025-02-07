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
    usuario_id: int  # Hereda todos los campos de ReporteEntregaBase

# Esquema para la actualización de un reporte de entrega
class ReporteEntregaUpdate(BaseModel):
    fecha_entrega: Optional[date]  # Fecha de entrega opcional
    estado: Optional[str]  # Estado opcional

# Esquema completo de reporte de entrega (incluye ID)
class ReporteEntrega(ReporteEntregaBase):
    entrega_id: int  # ID único del reporte

    class Config:
        from_attributes = True  # Permite convertir desde objetos SQLAlchemy
