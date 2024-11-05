from pydantic import BaseModel
from typing import Optional, List
from .productos import Producto #Importa el esquema de producto

class ProveedorBase(BaseModel):
    nombre: str
    email: Optional[str] = None
    telefono: Optional[str] = None
    direccion: Optional[str] = None

class ProveedorCreate(ProveedorBase):
    pass

class ProveedorUpdate(ProveedorBase):
    pass

class Proveedor(ProveedorBase):
    proveedor_id: int
    productos: List[Producto] = [] #Lista de productos relacionados con este proveedor

    class Config:
        from_attributes = True
