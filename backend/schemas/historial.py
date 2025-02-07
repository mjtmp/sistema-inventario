from pydantic import BaseModel
from datetime import datetime

class HistorialBase(BaseModel):
    usuario_id: int
    accion: str
    detalles: str = None

class HistorialCreate(HistorialBase):
    pass

class Historial(HistorialBase):
    historial_id: int
    fecha: datetime

    class Config:
        from_attributes = True
