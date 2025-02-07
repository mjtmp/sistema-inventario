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
    usuario_id: int  # Asegurar que usuario_id está incluido

# Esquema para actualizar una entrada de inventario
class EntradaInventarioUpdate(BaseModel):
    cantidad: Optional[int] = None  # Cantidad opcional para actualizar
    precio_compra: Optional[float] = None  # Precio de compra opcional para actualizar
    fecha: Optional[date] = None  # Fecha opcional para actualizar
    proveedor_id: Optional[int] = None  # ID de proveedor opcional para actualizar
    usuario_id: int  # Incluir usuario_id

# Esquema que representa una entrada de inventario completa
class EntradaInventario(EntradaInventarioBase):
    entrada_id: int  # ID único de la entrada de inventario

    
class EntradaInventarioResponse(BaseModel):
    entrada_id: int
    producto_id: int
    producto_nombre: str  # Añadir el nombre del producto
    proveedor_id: int
    proveedor_nombre: str  # Añadir el nombre del proveedor
    cantidad: float
    precio_compra: float
    fecha: date


class EntradaProductoResponse(BaseModel):
    producto: str
    total_entradas: int
    valor_entradas: float

class EntradaPorProductoFechaResponse(BaseModel):
    producto: str
    fecha: date
    cantidad: int

    class Config:
        from_attributes = True  # Permite que Pydantic use atributos directamente de la base de datos

