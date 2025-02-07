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
