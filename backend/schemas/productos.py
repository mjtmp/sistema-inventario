from pydantic import BaseModel
from typing import Optional

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str  # Nuevo campo 'descripcion'
    precio: float
    tiene_iva: bool
    stock: int
    proveedor_id: int  # Nuevo campo 'proveedor_id', que es una clave foránea

class ProductoCreate(ProductoBase):
    pass

class ProductoUpdate(ProductoBase):
    pass

class Producto(ProductoBase):
    producto_id: int

    class Config:
        from_attributes = True