<<<<<<< HEAD
from pydantic import BaseModel  # Base para crear esquemas de validación.
from typing import Optional  # Para campos opcionales.

# Esquema base para productos, define los campos comunes.
class ProductoBase(BaseModel):
    nombre: str  # Nombre del producto.
    descripcion: str  # Descripción del producto.
    precio: float  # Precio del producto.
    tiene_iva: bool  # Indica si el producto incluye IVA.
    stock: int  # Cantidad en inventario.
    proveedor_id: int  # ID del proveedor asociado (clave foránea).
    codigo_barras: Optional[str] = None  # Código de barras opcional.

# Esquema para crear productos, hereda del esquema base.
class ProductoCreate(ProductoBase):
    pass

# Esquema para actualizar productos, hereda del esquema base.
class ProductoUpdate(ProductoBase):
    pass

# Esquema para devolver productos, incluye el ID del producto.
class Producto(ProductoBase):
    producto_id: int  # ID único del producto.

    class Config:
        from_attributes = True  # Permite convertir modelos SQLAlchemy a Pydantic.
=======
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
>>>>>>> fcf9aa17a154f72265472b74da8da620bf9c1c39
