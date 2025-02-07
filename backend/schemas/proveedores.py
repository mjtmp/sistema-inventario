from pydantic import BaseModel
from typing import Optional, List
from .productos import Producto  # Importa el esquema relacionado con productos

# Clase base para proveedores
class ProveedorBase(BaseModel):
    nombre: str  # Nombre del proveedor
    email: Optional[str] = None  # Email del proveedor (opcional)
    telefono: Optional[str] = None  # Teléfono del proveedor (opcional)
    direccion: Optional[str] = None  # Dirección del proveedor (opcional)

# Esquema para crear proveedores (hereda de la base)
class ProveedorCreate(ProveedorBase):
    pass

# Esquema para actualizar proveedores (hereda de la base)
class ProveedorUpdate(ProveedorBase):
    pass

# Esquema para representar proveedores (incluye ID y productos relacionados)
class Proveedor(ProveedorBase):
    proveedor_id: int  # ID único del proveedor
    productos: List[Producto] = []  # Lista de productos asociados con el proveedor

    class Config:
        from_attributes = True  # Permite que Pydantic utilice atributos del modelo SQLAlchemy

