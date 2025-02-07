from pydantic import BaseModel
from typing import Optional
from schemas.categorias import Categoria

class ProductoBase(BaseModel):
    nombre: str
    descripcion: str
    precio: float
    tiene_iva: bool
    stock: int
    codigo: str
    proveedor_id: int
    codigo_barras: Optional[str] = None
    categoria_id: int  # Relación con categoría
    ubicacion: Optional[str] = None  # Nuevo campo
    cantidad_minima: Optional[int] = None  # Nuevo campo
    cantidad_maxima: Optional[int] = None  # Nuevo campo

class ProductoCreate(ProductoBase):
    usuario_id: int  # Asegurar que usuario_id está incluido

class ProductoUpdate(ProductoBase):
    usuario_id: int  # Incluir usuario_id

class Producto(ProductoBase):
    producto_id: int
    categoria: Optional[Categoria] = None  # Información completa de la categoría
    fecha_creacion: Optional[str] = None  # Cambiar tipo a str
    fecha_actualizacion: Optional[str] = None  # Cambiar tipo a str

class ProductoResponse(BaseModel):
    producto_id: int
    nombre: str
    descripcion: Optional[str] = None
    precio: float
    tiene_iva: bool
    stock: int
    proveedor_id: Optional[int] = None
    codigo_barras: Optional[str] = None
    categoria_id: Optional[int] = None
    fecha_creacion: Optional[str] = None
    fecha_actualizacion: Optional[str] = None
    ubicacion: Optional[str] = None  # Nuevo campo
    cantidad_minima: Optional[int] = None  # Nuevo campo
    cantidad_maxima: Optional[int] = None  # Nuevo campo

    class Config:
        from_attributes = True
