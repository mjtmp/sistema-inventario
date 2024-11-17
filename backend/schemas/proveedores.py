from pydantic import BaseModel
from typing import Optional, List
<<<<<<< HEAD
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

=======
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
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
