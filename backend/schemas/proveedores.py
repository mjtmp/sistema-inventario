from pydantic import BaseModel
from typing import Optional, List
from .productos import Producto

class ProveedorBase(BaseModel):
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None
    rif: Optional[str] = None  # Nuevo campo para el RIF

class ProveedorCreate(ProveedorBase):
    usuario_id: int  # Asegurar que usuario_id está incluido

class ProveedorUpdate(ProveedorBase):
    usuario_id: int  # Incluir usuario_id

class Proveedor(ProveedorBase):
    proveedor_id: int
    productos: List[Producto] = []
    fecha_creacion: Optional[str] = None  # Cambiar tipo a str
    fecha_actualizacion: Optional[str] = None  # Cambiar tipo a str

    class Config:
        from_attributes = True
