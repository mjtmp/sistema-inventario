from pydantic import BaseModel
from typing import Optional
from datetime import date

# Esquema base para las entradas de inventario
class EntradaInventarioBase(BaseModel):
    producto_id: int  # ID del producto
    cantidad: int  # Cantidad del producto en la entrada
    precio_compra: float  # Precio de compra del producto
    fecha: Optional[date] = date.today()  # Fecha de la entrada, por defecto es hoy
    proveedor_id: int  # ID del proveedor

# Esquema para crear una nueva entrada de inventario
class EntradaInventarioCreate(EntradaInventarioBase):
    pass

# Esquema para actualizar una entrada de inventario
class EntradaInventarioUpdate(BaseModel):
    cantidad: Optional[int] = None  # Cantidad opcional para actualizar
    precio_compra: Optional[float] = None  # Precio de compra opcional para actualizar
    fecha: Optional[date] = None  # Fecha opcional para actualizar
    proveedor_id: Optional[int] = None  # ID de proveedor opcional para actualizar

# Esquema que representa una entrada de inventario completa
class EntradaInventario(EntradaInventarioBase):
    entrada_id: int  # ID único de la entrada de inventario

# Esquema para la respuesta con información más detallada
class EntradaInventarioResponse(BaseModel):
    entrada_id: int  # ID único de la entrada
    producto_id: int  # ID del producto
    producto_nombre: str  # Nombre del producto (relación JOIN)
    proveedor_id: int  # ID del proveedor
    proveedor_nombre: str  # Nombre del proveedor (relación JOIN)
    cantidad: int  # Cantidad del producto
    precio_compra: float  # Precio de compra
    fecha: date  # Fecha de la entrada
    
    class Config:
        from_attributes = True  # Permite que Pydantic use atributos directamente de la base de datos

